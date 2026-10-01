import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")

URL = "https://openrouter.ai/api/v1/chat/completions"


def ask_ai(prompt):

    if not API_KEY:
        return "AI Error: OpenRouter API key missing."

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://resume-analyser-ns1e.onrender.com",
        "X-Title": "AI Resume Analyzer"
    }

    data = {
        "model": "openrouter/free",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.3,
        "max_tokens": 2000
    }

    try:
        response = requests.post(
            URL,
            headers=headers,
            json=data,
            timeout=(5, 20)
        )

        response.raise_for_status()

        result = response.json()

        if "choices" in result and len(result["choices"]) > 0:

            message = result["choices"][0].get("message", {})

            content = message.get("content")

            if content:
                return content

            return "⚠ AI returned an empty response."

        return "⚠ AI Error Response: " + str(result)

    except requests.Timeout:
        return (
            "⚠ AI service took too long to respond. "
            "The resume analysis was completed, but AI analysis is temporarily unavailable."
        )

    except requests.HTTPError as e:

        if e.response is not None:

            try:
                error_data = e.response.json()
            except Exception:
                error_data = e.response.text

            return f"⚠ OpenRouter API Error ({e.response.status_code}): {error_data}"

        return f"⚠ OpenRouter HTTP Error: {str(e)}"

    except requests.RequestException as e:
        return f"⚠ OpenRouter connection error: {str(e)}"

    except Exception as e:
        return f"⚠ AI Error: {str(e)}"


def get_complete_analysis(resume_text):

    prompt = f"""
You are an expert AI Resume Analyzer, ATS specialist, and technical interviewer.

Analyze the candidate's resume carefully.

IMPORTANT:
Your response MUST include ALL sections below.
Do NOT provide only a summary.
Do NOT skip the interview questions sections.

Keep the response concise but useful.

Return the answer in Markdown format.

# Candidate Summary

Write a short professional summary of the candidate based strictly on the resume.

# Technical Skills

Categorize the candidate's skills:

### Programming Languages
### Database
### Web Technologies
### AI/ML
### Frameworks
### Tools

# Strengths

Mention 4-5 important strengths visible from the resume.

# ATS Improvements

Give practical suggestions to improve the ATS score.

Focus on:
- Keywords
- Formatting
- Skills
- Projects
- Resume content

# Missing Skills

Mention important skills the candidate should learn based on their current skills, projects, and AI/ML career direction.

# Suggested Job Roles

Suggest suitable job roles based on the candidate's skills and projects.

# Technical Interview Questions

THIS SECTION IS REQUIRED.

Generate 10 technical interview questions specifically based on THIS resume.

The questions should cover:

1. Python
2. Java
3. SQL / Database
4. Flask / Web Development
5. AI / Machine Learning
6. APIs
7. Git / GitHub
8. Project-related questions
9. Computer Science fundamentals
10. Problem solving

For project-related questions, use the actual projects mentioned in the resume.

Format them as:

1. Question
2. Question
3. Question
...
10. Question

# HR Interview Questions

THIS SECTION IS REQUIRED.

Generate 5 HR interview questions suitable for this candidate.

Include questions such as:
- Tell me about yourself.
- Why should we hire you?
- Why did you choose AI/ML?
- What are your strengths and weaknesses?
- Where do you see yourself in the future?

Make the questions relevant to the candidate's resume.

# Project Interview Questions

THIS SECTION IS REQUIRED.

Generate 5 questions specifically about the candidate's projects.

Ask about:
- Project purpose
- Technologies used
- How the project works
- Challenges faced
- Future improvements

# Interview Preparation Tips

Give 5 short tips for preparing for an interview based on this resume.

IMPORTANT FINAL RULE:
The response MUST contain:
1. Candidate Summary
2. Technical Skills
3. Strengths
4. ATS Improvements
5. Missing Skills
6. Suggested Job Roles
7. Technical Interview Questions
8. HR Interview Questions
9. Project Interview Questions
10. Interview Preparation Tips

Do not omit any section.

Resume:

{resume_text}
"""

    return ask_ai(prompt)
