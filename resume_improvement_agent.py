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


logging.basicConfig(level=logging.INFO,format="%(asctime)s [%(levelname)s] %(message)s")

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
    template="""You are helping review a resume the way a careful recruiter would.

Read the candidate's resume and compare it with the target job description.

Look at what matches well, what is missing, and what could be clearer or stronger.

RESUME:
{resume}

TARGET JOB DESCRIPTION:
{job_description}

Please identify and prioritize:

1. Missing or weak keywords
   - Technical skills
   - Tools and platforms
   - Industry terms
   - Important responsibilities

2. Vague or weak statements
   - Generic responsibilities
   - Weak descriptions
   - Statements that do not show real value

3. Repeated content
   - Repeated skills
   - Repeated job duties
   - Repeated wording

4. Weak evidence
   - Claims that do not have enough detail
   - Missing impact or context where it could help
   - Areas that feel unclear or incomplete

5. Important skill gaps
   - Skills the job asks for but the resume does not clearly show
   - Separate these clearly:
       a) Missing from the resume
       b) Possibly relevant but not fully supported
       c) Already demonstrated

6. Priority level
   Rank the improvements as:
   HIGH
   MEDIUM
   LOW

Important rules:
- Do not assume the candidate has a skill just because it appears in the job description.
- Do not invent certifications, employers, projects, responsibilities, achievements, or metrics.
- If something is missing, say it is missing.
- Keep the feedback honest, practical, and easy to understand.

Return a clear Markdown gap analysis with the biggest issues first.
"""
)


REWRITE_PROMPT = PromptTemplate(
    input_variables=["gap_analysis", "resume"],
    template="""You are helping improve a resume in a natural, honest, and practical way.

Use the gap analysis below to strengthen the resume without making anything up.

GAP ANALYSIS:
{gap_analysis}

ORIGINAL RESUME:
{resume}

Rewrite the following sections where it helps:

1. Professional Summary
2. Technical Skills
3. Professional Experience bullets

Please do this in a simple, professional, recruiter-friendly style:
- Keep the wording clear and direct
- Use strong action verbs
- Focus on real experience already in the resume
- Improve relevance to the target role when it is truthful
- Remove repetition and weak wording
- Make the bullet points more specific and easier to read
- Keep the candidate's actual background and experience intact

Important rules:
- Do not invent skills, projects, technologies, certifications, or experience.
- Do not make up numbers, metrics, business outcomes, or achievements.
- If a metric or result is not mentioned, do not create one.
- If a skill is missing, do not pretend it exists.
- Only use information that is already supported by the original resume.

Return only the improved resume sections in Markdown.

Use this format:

## Professional Summary

...

## Technical Skills

...

## Professional Experience

### [Company / Role]

- ...
- ...
- ...

Do not include any extra explanation outside the rewritten sections.
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



SYSTEM_PROMPT = """You are helping a candidate improve their resume for a specific job in a realistic and honest way.

You have two tools available:

1. analyze_resume_gaps
2. rewrite_resume_sections

The correct flow is:

Step 1:
Read the full resume and the full job description, then call analyze_resume_gaps.

Step 2:
Use the results from that analysis and the original resume to call rewrite_resume_sections.

Step 3:
Return the rewritten resume sections to the user.

Important:
- Do not rewrite before doing the analysis.
- Do not make up skills, experience, certifications, projects, or metrics.
- Only use details that are already in the candidate's original resume.
- A keyword in the job description does not automatically mean the candidate has that skill.
- If something is missing, keep it missing instead of inventing it.
- Improve clarity, relevance, and impact while staying truthful.
- The final output should be the improved resume sections in Markdown.
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