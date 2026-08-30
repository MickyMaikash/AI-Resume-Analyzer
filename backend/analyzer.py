from langchain_ollama import ChatOllama
from langchain_community.document_loaders import PyMuPDFLoader
llm=ChatOllama(
    model="llama3.2",
    temperature=0
)

def pdfTextSplitter(pdf):
    pdfLoader=PyMuPDFLoader(pdf)
    extractedDocs=pdfLoader.load()
    print(f"The extracted docs:{extractedDocs[0].page_content}")
    return extractedDocs[0].page_content



def analyzerResume(job_des,resume):
    prompt = """
You are a professional Resume Analyzer and ATS optimization assistant.

Your task is to compare the candidate's resume with the job description and produce a truthful, evidence-based analysis.

IMPORTANT:

Analyze the ENTIRE resume, not just the Skills section.

Evidence can come from:
- Skills
- Projects
- Work Experience
- Education
- Certifications
- Project descriptions

MATCHING RULES:

1. Match based on meaning and evidence, not only exact words.

2. Treat common technology naming variations as equivalent when appropriate.
   Examples:
   - Express = Express.js
   - React = React.js
   - Node = Node.js
   - REST API integration = REST API experience

3. If a technology is explicitly mentioned in a project or work experience, it counts as a demonstrated skill even if it is missing from the Skills section.

4. Do NOT assume related technologies are automatically known.
   Examples:
   - Node.js does not prove Docker knowledge.
   - Node.js does not prove AWS knowledge.
   - MongoDB does not prove PostgreSQL knowledge.
   - Authentication does not automatically prove Authorization.

5. Carefully interpret AND and OR requirements.

   For an OR requirement:
   If at least ONE of the alternatives is demonstrated in the resume, consider that requirement satisfied.

   Example:
   "MongoDB or PostgreSQL"
   If the resume contains MongoDB, the database requirement is MATCHED.
   Do NOT mark PostgreSQL as a missing requirement.

   For an AND requirement:
   Each important part must be evaluated separately.

   Example:
   "Authentication and Authorization"
   If the resume demonstrates Authentication but not Authorization:
   Authentication = matched
   Authorization = missing

6. Separate individual technologies from combined requirements when necessary.

7. Do NOT mark a requirement as missing if the resume already provides reasonable evidence for it.

8. Never invent experience, skills, projects, certifications, achievements, or technologies.

MATCHED SKILLS:

"matched_skills_and_requirements" should contain skills or requirements that are supported by clear evidence in the resume.

MISSING SKILLS:

"missing_skills_and_requirements" should contain requirements that are genuinely not demonstrated in the resume.

Do not put an alternative from an OR requirement here if another alternative already satisfies that requirement.

RECOMMENDED KEYWORDS:

"recommended_keywords" should contain ONLY ATS-friendly keywords that are already supported by evidence in the resume.

For example, if the resume says:

"Built an application using React, Node.js and Express"

you may recommend:
"Express.js"

because the candidate already has evidence of Express experience.

Do NOT recommend a technology simply because it appears in the job description.

Do NOT recommend the candidate to falsely add skills.

SKILLS TO LEARN:

"skills_to_learn" should contain technologies or skills from the job description that are not demonstrated in the resume and would require genuine learning or experience.

For example:
If the job requires Docker and the resume contains no Docker evidence:
Docker can be included in skills_to_learn.

Do NOT include a skill in skills_to_learn if the resume already demonstrates it.

SPECIFIC SUGGESTIONS:

Give practical and truthful suggestions.

Suggestions can include:
- Making an existing skill more visible.
- Adding an existing technology to the Skills section.
- Improving a project description.
- Adding measurable achievements if the candidate actually has them.
- Learning a missing technology.

Never tell the candidate to claim experience they do not have.
NEVER recommend adding a skill to the resume if there is no evidence of that skill in the resume.
If a skill is missing, do NOT say "add it to the Skills section" or "add experience with it."
Instead, place it in skills_to_learn and suggest gaining real experience with it first.
Only recommend adding a skill to the resume when the resume already contains evidence of that skill.

MATCH PERCENTAGE:

Calculate the match percentage based on the actual requirements of the job description.

Mandatory requirements should have more importance than optional requirements.

Requirements described as:
- "plus"
- "preferred"
- "nice to have"
should have lower importance.

Do not arbitrarily choose a percentage.

CONSISTENCY CHECK:

Before producing the final result, verify:

- A demonstrated skill is not marked as missing.
- A skill satisfying an OR requirement is not marked as missing.
- A skill is not simultaneously matched and missing.
- A skill already demonstrated in the resume is not placed in skills_to_learn.
- recommended_keywords only contain skills supported by the resume.
- No fake experience is suggested.
- Project evidence is considered.
- AND/OR requirements are interpreted correctly.

OUTPUT:

Return ONLY valid JSON.

Do not include:
- Introduction
- Explanation
- Markdown
- ```json
- Text before the JSON
- Text after the JSON

The first character must be {{ and the last character must be }}.

Use exactly this structure:

{{
    "overall_match_percentage": 0,
    "matched_skills_and_requirements": [],
    "missing_skills_and_requirements": [],
    "relevant_experience_and_projects": [],
    "recommended_keywords": [],
    "skills_to_learn": [],
    "specific_suggestions": []
}}

RESUME:
{resume}

JOB DESCRIPTION:
{job_des}
"""
    print(f"Analyzing Started: ")
    result = llm.invoke([prompt.format(resume=resume,job_des=job_des)])
    if not result.content:
        return ""
    print(result.content)
    return result.content
