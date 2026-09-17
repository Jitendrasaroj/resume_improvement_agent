# Resume Improvement Agent

An AI-powered **Resume Improvement Agent** built with **LangChain and OpenAI** that reviews a resume against a target job description, identifies gaps, and rewrites relevant resume sections for better relevance, clarity, and impact.

The agent is designed with an **ethical resume-writing workflow**: it improves how existing experience is presented without fabricating skills, certifications, projects, achievements, metrics, or work experience.

---

## 🚀 Features

* 📄 Analyze a resume against a target Job Description (JD)
* 🔍 Identify missing and underrepresented keywords
* 📝 Detect vague or weak resume statements
* 🔄 Identify repetitive skills and responsibilities
* 📊 Highlight areas with weak supporting evidence
* 🎯 Identify relevant skill gaps
* ⭐ Prioritize improvements as:

  * `HIGH`
  * `MEDIUM`
  * `LOW`
* ✨ Rewrite:

  * Professional Summary
  * Technical Skills
  * Professional Experience bullets
* 🛡️ Prevent fabricated skills, experience, certifications, projects, and metrics
* 🤖 Uses a LangChain agent with two dedicated tools
* 💻 Supports interactive CLI input

---

## 🏗️ Architecture

```text
                    ┌─────────────────────┐
                    │       User          │
                    │                     │
                    │ Resume + Job Desc.  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  LangChain Agent    │
                    │                     │
                    │  Mandatory Tool     │
                    │      Ordering        │
                    └──────────┬──────────┘
                               │
                               ▼
              ┌────────────────────────────────┐
              │     Tool 1                     │
              │     analyze_resume_gaps        │
              │                                │
              │ • Missing keywords             │
              │ • Vague statements             │
              │ • Repetition                   │
              │ • Weak evidence                │
              │ • Skill gaps                   │
              │ • Priority                     │
              └───────────────┬────────────────┘
                              │
                              │ Gap Analysis
                              ▼
              ┌────────────────────────────────┐
              │     Tool 2                     │
              │     rewrite_resume_sections    │
              │                                │
              │ • Professional Summary         │
              │ • Technical Skills             │
              │ • Experience bullets           │
              └───────────────┬────────────────┘
                              │
                              ▼
                    ┌─────────────────────┐
                    │ Improved Resume     │
                    │ Sections (Markdown) │
                    └─────────────────────┘
```

---

## 🧰 Tools

The agent contains exactly two tools.

### 1. `analyze_resume_gaps`

Analyzes the candidate's resume against the target job description.

#### Input

```text
resume
job_description
```

#### Identifies

* Missing or underrepresented technical skills
* Tools and platforms
* Domain terminology
* Relevant responsibilities
* Vague statements
* Repeated content
* Weak evidence
* Relevant skill gaps
* Improvement priorities

#### Output

A structured Markdown gap analysis.

Example:

```markdown
## HIGH Priority

- Python is mentioned but Python automation projects are not clearly described.
- API integration experience is present but not highlighted in the summary.

## MEDIUM Priority

- Professional experience contains repetitive descriptions of automation activities.

## LOW Priority

- Some bullet points can be shortened for better readability.
```

---

### 2. `rewrite_resume_sections`

Uses the gap analysis and original resume to rewrite relevant sections.

#### Input

```text
gap_analysis
resume
```

#### Rewrites

```text
Professional Summary
Technical Skills
Professional Experience
```

#### Output

Markdown containing only the improved resume sections.

---

## 🔄 Mandatory Agent Workflow

The agent enforces the following tool sequence:

```text
Resume + Job Description
          │
          ▼
analyze_resume_gaps
          │
          ▼
    Gap Analysis
          │
          ▼
rewrite_resume_sections
          │
          ▼
 Improved Resume
```

### Important

`rewrite_resume_sections` must **never** be called before `analyze_resume_gaps`.

The system prompt explicitly instructs the LangChain agent to follow this order.

---

## 🛡️ Ethical Resume Improvement

A major design goal of this project is to improve resume quality **without misrepresenting the candidate**.

The agent follows these rules:

### ❌ It does not invent

* Skills
* Technologies
* Certifications
* Employers
* Projects
* Responsibilities
* Achievements
* Metrics
* Percentages
* Revenue
* Cost savings
* Team sizes
* Processing volumes
* Performance improvements
* Business outcomes

### ✅ It can improve

* Wording
* Clarity
* Structure
* Relevance
* Action verbs
* Conciseness
* Keyword visibility
* Description of already-supported experience

For example:

**Original**

```text
Worked on automation projects using Python.
```

**Improved**

```text
Developed Python-based automation solutions to streamline recurring business processes.
```

The improvement changes the wording but does not introduce an unsupported technology, metric, or achievement.

---

## 📁 Project Structure

A simple project structure can be:

```text
resume-improvement-agent/
│
├── resume_improvement_agent.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## ⚙️ Requirements

* Python 3.9+
* OpenAI API key
* LangChain
* LangChain OpenAI integration
* python-dotenv

---

## 📦 Installation

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd resume-improvement-agent
```

### 2. Create a virtual environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 Configure OpenAI API Key

Create a `.env` file based on `.env.example`.

### `.env.example`

```env
OPENAI_API_KEY=sk-your-api-key
```

Then add your actual API key:

```env
OPENAI_API_KEY=your-openai-api-key
```

> **Never commit your `.env` file or API key to GitHub.**

Add this to `.gitignore`:

```gitignore
.env
venv/
__pycache__/
*.pyc
```

---

## ▶️ Run the Agent

Run:

```bash
python resume_improvement_agent.py
```

You will see:

```text
======================================================================
RESUME IMPROVEMENT AGENT
LangChain + OpenAI
======================================================================

Paste your resume.
Type END on a new line when finished.
```

Paste your resume and type:

```text
END
```

Then paste the target job description and type:

```text
END
```

The agent will process both inputs and return the improved resume sections.

---

## 💡 Example

### Resume

```text
John Doe

Professional Summary:
Automation developer with experience in RPA and Python.

Skills:
Python, UiPath, SQL, API

Experience:

ABC Technologies
Automation Developer

- Worked on automation projects.
- Developed Python scripts.
- Worked with APIs.
- Fixed production issues.
```

### Target Job Description

```text
We are looking for an Automation Developer with experience in:

- Python
- REST APIs
- SQL
- Automation frameworks
- Production support
- Cloud technologies
```

### Agent Process

```text
Resume
   +
Job Description
   │
   ▼
Gap Analysis
   │
   ├── Python → Demonstrated
   ├── REST APIs → Demonstrated
   ├── SQL → Demonstrated
   ├── Production support → Demonstrated
   ├── Automation frameworks → Partially supported
   └── Cloud technologies → Missing
   │
   ▼
Resume Rewrite
```

### Example Output

```markdown
## Professional Summary

Automation Developer with experience building Python and RPA-based
automation solutions, integrating APIs, working with SQL, and supporting
production automation processes.

## Technical Skills

- Automation: RPA, UiPath
- Programming: Python, SQL
- Integration: REST APIs
- Support: Production troubleshooting and issue resolution

## Professional Experience

### ABC Technologies — Automation Developer

- Developed Python-based automation scripts to streamline recurring business processes.
- Integrated APIs into automation workflows.
- Worked with SQL for automation and data-related requirements.
- Supported production automation workflows and resolved operational issues.
```

Notice that **cloud technologies were not added**, because the original resume did not demonstrate them.

---

## 🧠 Prompt Design

The project uses two specialized prompts.

### Analysis Prompt

The analysis prompt focuses on:

```text
Resume
   ↓
Job Description Comparison
   ↓
Gap Identification
   ↓
Prioritization
```

It specifically distinguishes between:

```text
Missing from Resume
        │
        ├── Possibly Relevant but Unsupported
        │
        └── Already Demonstrated
```

This helps prevent the agent from treating every keyword in the JD as a skill possessed by the candidate.

---

### Rewrite Prompt

The rewrite prompt focuses on:

```text
Original Resume
      +
Gap Analysis
      │
      ▼
Improved Resume Sections
```

It uses only information supported by the original resume.

---

## 🤖 Model Configuration

The current implementation uses:

```python
llm = ChatOpenAI(
    model="gpt-4.1-mini",
    temperature=0.7
)
```

You can change the model based on your requirements.

For example:

```python
llm = ChatOpenAI(
    model="your-model",
    temperature=0.7
)
```

---

## 🔧 Main Function

The main reusable function is:

```python
run_resume_improvement(
    resume=resume,
    job_description=job_description
)
```

This makes the agent easy to integrate into another application.

For example:

```python
improved_resume = run_resume_improvement(
    resume=my_resume,
    job_description=my_job_description
)

print(improved_resume)
```

---

## 🧩 Potential Integrations

The agent can be extended into:

* 🌐 Web application
* 💬 Chatbot
* 📄 Resume upload application
* 🔗 LinkedIn profile analyzer
* 📊 Resume scoring dashboard
* 📧 Job application assistant
* 🏢 Internal recruitment platform
* 🔄 Automated resume customization pipeline

Possible future workflow:

```text
Resume PDF/DOCX
      │
      ▼
Text Extraction
      │
      ▼
Resume Improvement Agent
      │
      ├── Gap Analysis
      │
      └── Resume Rewrite
      │
      ▼
Formatted Resume
      │
      ▼
PDF / DOCX
```

---

## 🚀 Future Enhancements

Potential improvements include:

### Resume File Support

Support:

```text
PDF
DOCX
TXT
```

instead of requiring CLI text input.

### Job Description URL

Allow users to provide a job posting URL and automatically extract the JD.

### ATS Analysis

Add analysis for:

* Keyword coverage
* Section structure
* Formatting
* Job-specific terminology
* ATS-friendly wording

### Multiple Resume Versions

Generate role-specific versions:

```text
Resume
   │
   ├── Python Developer Version
   ├── RPA Developer Version
   ├── Automation Engineer Version
   └── AI Automation Version
```

### Structured Output

Return JSON containing:

```json
{
  "gap_analysis": {},
  "missing_skills": [],
  "demonstrated_skills": [],
  "rewritten_sections": {}
}
```

---

## ⚠️ Limitations

The agent improves the resume based on the information provided to it.

It cannot reliably determine that a candidate possesses a skill simply because:

* The skill appears in the job description.
* The skill is commonly associated with the candidate's role.
* A similar technology appears in the resume.
* The candidate may have learned the skill outside their listed experience.

Therefore, missing information remains missing unless the candidate provides supporting information.

---

## 🔒 Security

Never commit sensitive information.

Do not commit:

```text
.env
API keys
Personal access tokens
Private resumes
Confidential job descriptions
```

Recommended `.gitignore`:

```gitignore
.env
venv/
.venv/
__pycache__/
*.pyc
```

---

## 📜 License

Add the license appropriate for your project.

Example:

```text
MIT License
```

---

## 👨‍💻 Author

**Jitendra Saroj**

Built using:

* Python
* LangChain
* OpenAI
* LangChain Agents
* Prompt Engineering
* AI-powered Resume Optimization
