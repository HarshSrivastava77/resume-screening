import os
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq

from pydantic import BaseModel,Field

from pypdf import PdfReader
from docx import Document

load_dotenv()
my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("GROQ_API_KEY not found.")

client = Groq(api_key = my_api_key)
##########Why model = MODEL_NAME,Why use a variable??
#Answer:-

##Instead of writing the model name everywhere,

##change it in one place.

##Follows the DRY (Don't Repeat Yourself) principle.

MODEL_NAME = "openai/gpt-oss-120b" 
#Define the Pydantic model for the expected output structure
class JobD(BaseModel):
    role:str
    required_skills : list[str]
    preferred_skills : list[str]
    minimum_experience : float|None
    educational_requirements : list[str]
    responsibilities : list[str]

#Pyadantic Model -> JSON Schema coz The LLM doesn't understand Python classes.
jobd_schema = JobD.model_json_schema()

system_prompt = f"""
You are an expert HR assistant.

Your task is to extract structured information
from the given job description.

Return ONLY valid JSON matching this schema.

Schema:

{jobd_schema}

Rules:

- Do not return markdown.
- Do not explain anything.
- Do not invent information.
- If a field is missing, return null or an empty list.
"""
job_description = """
Software Development Engineer (SDE) Intern

Location: Bengaluru / Hyderabad / Pune / Gurgaon

Duration: 3–6 Months

Stipend: ₹80,000 – ₹2,00,000/month

About the Role

We are looking for highly motivated Software Development Engineer Interns who are passionate about solving complex engineering problems and building scalable software systems. You will work alongside experienced engineers to design, develop, test, and deploy production-quality software used by millions of users.

Responsibilities
Design, develop, test, and maintain scalable software applications.
Write clean, efficient, and maintainable code following software engineering best practices.
Solve algorithmic and system-level problems.
Participate in code reviews and design discussions.
Optimize application performance and reliability.
Build RESTful APIs and backend services.
Work with relational and NoSQL databases.
Debug production issues and improve system stability.
Collaborate with product managers, designers, and engineers.
Write unit and integration tests.
Contribute throughout the complete Software Development Life Cycle (SDLC).
Required Qualifications
Education
Pursuing B.E./B.Tech in Computer Science or related field.
Expected graduation between 2027–2028.
CGPA 8.0+ preferred.
Required Skills
Programming Languages
C++
Java
Python
Go (Preferred)
Data Structures & Algorithms

Strong understanding of

Arrays
Strings
Linked Lists
Stacks
Queues
Trees
Binary Search Trees
Heaps
Hash Maps
Graphs
Dynamic Programming
Greedy Algorithms
Backtracking
Binary Search
Sliding Window
Two Pointer Technique
Recursion
Computer Science Fundamentals
Object-Oriented Programming
Operating Systems
Computer Networks
Database Management Systems
SQL
Computer Architecture
Multithreading
Concurrency
Software Engineering
Design Patterns
SOLID Principles
Clean Code
Debugging
Unit Testing
Version Control (Git)
Databases
MySQL
PostgreSQL
MongoDB
Redis
Backend Development

Experience with one or more

FastAPI
Flask
Django
Spring Boot
Node.js
API Development
REST APIs
JSON
HTTP
Authentication
JWT
Tools
Git
GitHub
Docker
Linux
VS Code
Cloud (Preferred)
AWS
Google Cloud
Azure
System Design (Basic)

Understanding of

Scalability
Load Balancing
Caching
Microservices
Database Sharding
CAP Theorem
Message Queues
Preferred Qualifications
Strong problem-solving skills.
300+ DSA problems solved on LeetCode/Codeforces.
Knowledge of Competitive Programming.
Open-source contributions.
Internship/project experience.
Strong communication skills.
Experience building full-stack applications.
Familiarity with Agile methodologies.
Nice-to-Have Projects
URL Shortener
Chat Application
Distributed Cache
Task Scheduler
E-commerce Backend
Library Management System
Banking Application
File Storage System
REST API Service
Online Judge
Social Media Backend
Parking Lot System
Hotel Booking System
Ride Sharing System
Interview Process
Round 1 – Online Assessment
DSA (Medium–Hard)
MCQs on CS Fundamentals
Coding (2–3 Questions)
Round 2 – Technical Interview

Topics

Arrays
Trees
Graphs
Dynamic Programming
Binary Search
Hashing
OOP
SQL
Round 3 – Technical Interview

Topics

Low-Level Design (LLD)
Object-Oriented Design
REST APIs
Database Design
Debugging
Round 4 – Hiring Manager / Behavioral
Leadership
Teamwork
Problem Solving
Ownership
Communication
What We Look For
Excellent coding ability.
Strong analytical thinking.
Passion for building scalable systems.
Curiosity to learn new technologies.
Ability to work independently and collaboratively.
Strong debugging and optimization skills.
Good communication and teamwork.

"""

user_prompt = f"""
Analyze the following job description.

{job_description}
"""

message_system = {
    "role":"system",
    "content":system_prompt
}

message_user = {
    "role":"user",
    "content" : user_prompt
}
messages = [message_system,message_user]

response = client.chat.completions.create(
    model = MODEL_NAME,
    messages = messages,
    response_format = {"type":"json_object"}
)

answer = response.choices[0].message.content
print("========== LLM Output ==========")
print(answer)

job = JobD.model_validate_json(answer)

print("\n=========Parsed Object=======")
print(job)

print("\nRole:",job.role)
print("Required Skills:",job.required_skills)
print("Preferred Skills:",job.preferred_skills)
print("Minimum Experience:",job.minimum_experience)
print("Educational Requirements:",job.educational_requirements)
print("Responsibilities:",job.responsibilities)

########Experience model
class Experience(BaseModel):
    company: str | None = None
    role: str | None = None
    duration: str | None = None
    description: str | None = None
    skills_used: list[str] = []

########### Resume Model
class Resume(BaseModel):
    name: str | None = None
    email: str | None = None
    phone: str | None = None

    total_experience_years: float | None = None

    skills: list[str] = []

    experiences: list[Experience] = []

    education: list[str] = []

    projects: list[str] = []

    certifications: list[str] = []

resume_schema = Resume.model_json_schema()

###Build parse_resume() Function
def parse_resume(resume_text:str) -> Resume:
    system_prompt = f"""
    You are an expert resume parser.

    Extract structured information from the resume.

    Return ONLY valid JSON matching this schema.

    Schema:

    {resume_schema}

    Rules:

    - Do not invent information.
    - If a value is missing, return null.
    - If a list has no values, return an empty list.
    - Include internships inside experiences.
    - Extract skills from the entire resume.
    """

    user_prompt = f"""
    Parse the following resume:

    {resume_text}
"""
    messages = [
    {
        "role": "system",
        "content": system_prompt
    },
    {
        "role": "user",
        "content": user_prompt
    }
]
    response = client.chat.completions.create(
    model=MODEL_NAME,
    messages=messages,
    response_format={
        "type": "json_object"
    }
)
    answer = response.choices[0].message.content
    resume = Resume.model_validate_json(answer)

    return resume

def read_pdf(file_path: Path) -> str:
    reader = PdfReader((file_path))
    text = ""  ## empty sttering to store the extracted text
    for page in reader.pages:
        text += (page.extract_text() or "") + "\n"
    return text

def read_docx(file_path: Path) -> str:
    doc = Document(file_path)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text


def read_resume(file_path: Path) -> str:

    suffix = file_path.suffix.lower()

    if suffix == ".pdf":
        return read_pdf(file_path)

    elif suffix == ".docx":
        return read_docx(file_path)

    else:
        raise ValueError(f"Unsupported file format: {suffix}")

resume_path = Path("Enter the resume path here")  # Replace with the actual path to the resume file

resume_text = read_resume(resume_path)

resume = parse_resume(resume_text)

print("\n========== Parsed Resume ==========")
print(resume)

print("\nName:", resume.name)
print("Email:", resume.email)
print("Phone:", resume.phone)
print("Skills:", resume.skills)
print("Education:", resume.education)
print("Projects:", resume.projects)
print("Certifications:", resume.certifications)
print("Experiences:", resume.experiences)
    

class MatchResult(BaseModel):
    overall_score: float

    matched_skills: list[str]

    missing_skills: list[str]

    strengths: list[str]

    weaknesses: list[str]

    recommendation: str

match_schema = MatchResult.model_json_schema()

def match_resume(job: JobD, resume: Resume) -> MatchResult:

    system_prompt = f"""
    You are an expert technical recruiter.

    Compare the job requirements with the candidate's resume.

    Return ONLY valid JSON matching this schema.

    Schema:

    {match_schema}

    Rules:

    - Base your evaluation only on the provided information.
    - Do not invent experience or skills.
    - Consider transferable skills when appropriate.
    - Provide a realistic overall score between 0 and 100.
    """
    user_prompt = f"""
Compare the following job requirements and candidate resume.

Job:

{job.model_dump_json(indent=2)}

Resume:

{resume.model_dump_json(indent=2)}
"""
    messages = [
    {
        "role": "system",
        "content": system_prompt
    },
    {
        "role": "user",
        "content": user_prompt
    }
]
    response = client.chat.completions.create(
    model=MODEL_NAME,
    messages=messages,
    response_format={
        "type": "json_object"
    }
)  
    answer = response.choices[0].message.content
    result = MatchResult.model_validate_json(answer)
    return result

result = match_resume(job, resume)

print("\n========== Match Result ==========")
print(result)

print("\nOverall Score:", result.overall_score)

print("\nMatched Skills:")
print(result.matched_skills)

print("\nMissing Skills:")
print(result.missing_skills)

print("\nStrengths:")
print(result.strengths)

print("\nWeaknesses:")
print(result.weaknesses)

print("\nRecommendation:")
print(result.recommendation)