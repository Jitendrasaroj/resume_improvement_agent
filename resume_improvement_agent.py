"""
Resume Improvement Agent — a LangChain agent that reviews a resume
against a target job description and rewrites weak sections.

Setup:
    pip install -r requirements.txt
    copy .env.example to .env
    add your OpenAI API key

Run:
    python resume_improvement_agent.py
"""

import logging
import os
import sys

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI


# ----------------------------------------------------------------------
# Setup
# ----------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logger = logging.getLogger("resume_improvement_agent")

load_dotenv()

if not os.getenv("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY").startswith("sk-your"):
    logger.error(
        "OPENAI_API_KEY not set. Copy .env.example to .env and add your key."
    )
    sys.exit(1)


llm = ChatOpenAI(
    model="gpt-4.1-mini",
    temperature=0.7
)




ANALYZE_PROMPT = PromptTemplate(
    input_variables=["resume", "job_description"],
    template="""You are an ethical technical recruiter.

Review the candidate's resume against the target job description.

RESUME:
{resume}

TARGET JOB DESCRIPTION:
{job_description}

Identify and prioritize:

1. Missing or underrepresented keywords
   - Technical skills
   - Tools/platforms
   - Domain terminology
   - Relevant responsibilities

2. Vague statements
   - Generic responsibilities
   - Weak descriptions
   - Statements without clear outcomes

3. Repetition
   - Repeated skills
   - Repeated responsibilities
   - Duplicate wording

4. Weak evidence
   - Claims that lack supporting details
   - Missing measurable impact where the resume already provides evidence
   - Missing context around projects or responsibilities

5. Relevant skill gaps
   - Skills explicitly requested in the job description but not demonstrated
   - Clearly distinguish between:
       a) Missing from the resume
       b) Possibly relevant but unsupported
       c) Already demonstrated

6. Priorities
   Rank the improvements as:
   HIGH
   MEDIUM
   LOW

IMPORTANT ETHICAL RULES:
- Never assume the candidate has a skill simply because it appears in the job description.
- Never invent certifications.
- Never invent employers, projects, responsibilities, achievements, or metrics.
- Never create numbers that are not supported by the resume.
- If a job requirement is missing from the resume, explicitly say it is missing.

Return a structured Markdown gap analysis.
"""
)


REWRITE_PROMPT = PromptTemplate(
    input_variables=["gap_analysis", "resume"],
    template="""You are an ethical technical recruiter and professional resume writer.

Rewrite the candidate's resume sections using the gap analysis below.

GAP ANALYSIS:
{gap_analysis}

ORIGINAL RESUME:
{resume}

Rewrite the following sections where relevant:

1. Professional Summary
2. Technical Skills
3. Professional Experience bullets

Writing requirements:
- Use concise, impact-first language.
- Make bullets specific and recruiter-friendly.
- Prefer strong action verbs.
- Prioritize skills that are genuinely demonstrated in the original resume.
- Align wording with the target role where truthful.
- Preserve the candidate's actual experience.
- Improve clarity and relevance.
- Remove unnecessary repetition.
- Strengthen weak wording using only information already supported by the resume.

ETHICAL REQUIREMENTS:
- NEVER fabricate skills.
- NEVER fabricate experience.
- NEVER fabricate projects.
- NEVER fabricate certifications.
- NEVER fabricate technologies.
- NEVER invent metrics.
- NEVER invent percentages, savings, revenue, team size, processing volume,
  performance improvements, or business outcomes.
- If an impact metric is not available, improve the wording without creating one.
- Do not convert an unsupported skill gap into an implied skill.
- Do not claim the candidate used a technology merely because it appears
  in the target role.

Return ONLY the improved resume sections in Markdown.

Use this structure:

## Professional Summary

...

## Technical Skills

...

## Professional Experience

### [Company / Role]

- ...
- ...
- ...

Do not add explanations outside the rewritten resume sections.
"""
)


@tool
def analyze_resume_gaps(resume: str, job_description: str) -> str:
    """
    Analyze a resume against a target job description.

    """
    return llm.invoke(ANALYZE_PROMPT.format(resume=resume,job_description=job_description)).content




@tool
def rewrite_resume_sections(gap_analysis: str,resume: str) -> str:
    """
    Rewrite resume summary, skills, and experience using the gap analysis.

    This tool MUST be called only after analyze_resume_gaps.
    """
    return llm.invoke(REWRITE_PROMPT.format(gap_analysis=gap_analysis,resume=resume)).content



SYSTEM_PROMPT = """You are an ethical technical recruiter helping candidates
improve their resumes for specific target roles.

You have exactly two tools:

1. analyze_resume_gaps
2. rewrite_resume_sections

MANDATORY TOOL ORDER:

Step 1:
Always call analyze_resume_gaps first using the complete resume and
target job description.

Step 2:
After receiving the gap analysis, call rewrite_resume_sections using:
- the original resume
- the complete gap analysis from Tool 1

Step 3:
Return the output from rewrite_resume_sections to the user.

IMPORTANT:
- NEVER call rewrite_resume_sections before analyze_resume_gaps.
- NEVER fabricate skills, experience, certifications, projects, or metrics.
- Only use information supported by the candidate's original resume.
- A keyword appearing in the job description does NOT mean the candidate
  possesses that skill.
- Missing skills should remain missing rather than being invented.
- Improve wording, relevance, clarity, and impact while preserving truth.
- The final response must contain the improved resume sections in Markdown.
"""


agent = create_agent(model=llm,tools=[analyze_resume_gaps,rewrite_resume_sections],system_prompt=SYSTEM_PROMPT)



def run_resume_improvement(resume: str,job_description: str) -> str:
    """
    Run the Resume Improvement Agent.
    """

    user_request = f"""
    Please review my resume against the target job description
    and improve the relevant resume sections.

    RESUME:
    {resume}

    TARGET JOB DESCRIPTION:
    {job_description}
    """

    result = agent.invoke({"messages": [HumanMessage(content=user_request)]})
    return result["messages"][-1].content


# ----------------------------------------------------------------------
# CLI
# ----------------------------------------------------------------------

def main() -> None:

    print("\n" + "=" * 70)
    print("RESUME IMPROVEMENT AGENT")
    print("LangChain + OpenAI")
    print("=" * 70)

    print("\nPaste your resume.")
    print("Type END on a new line when finished.\n")

    resume_lines = []

    while True:
        line = input()

        if line.strip().lower() in ("quit", "exit", "q", "end"):
            break

        resume_lines.append(line)

    resume = "\n".join(resume_lines).strip()

    if not resume:
        print("Resume cannot be empty.")
        return

    print("\nPaste the target job description.")
    print("Type END on a new line when finished.\n")

    job_lines = []

    while True:
        line = input()

        if line.strip().lower() in ("quit", "exit", "q", "end"):
            break

        job_lines.append(line)

    job_description = "\n".join(job_lines).strip()

    if not job_description:
        print("Job description cannot be empty.")
        return

    try:

        logger.info("Starting resume improvement agent...")

        improved_resume = run_resume_improvement(
            resume=resume,
            job_description=job_description
        )

        print("\n" + "=" * 70)
        print("IMPROVED RESUME")
        print("=" * 70)
        print(improved_resume)
        print("=" * 70 + "\n")

    except Exception as e:

        logger.exception("Agent failed")

        print(f"\nAgent failed: {e}")


# ----------------------------------------------------------------------
# Entry Point
# ----------------------------------------------------------------------

if __name__ == "__main__":
    main()