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
        "max_tokens": 1200
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
You are an expert AI Resume Analyzer and ATS specialist.

Analyze the given resume professionally.

Keep the response concise so it can be generated quickly.

Provide the output in Markdown format.

Include these sections:

# Candidate Summary

Give a short professional overview of the candidate.

# Technical Skills

Separate skills into categories:

Programming Languages:
Database:
Web Technologies:
AI/ML:
Frameworks:
Tools:

# Strengths

Mention the strongest points of the resume.

# ATS Improvements

Give practical suggestions to improve ATS score.

Focus on:
- Keywords
- Formatting
- Projects
- Skills

# Missing Skills

Mention important missing skills according to current industry requirements.

# Suggested Job Roles

Suggest suitable roles for this candidate.

# Technical Interview Questions

Generate a few interview questions based on:
- Programming
- AI/ML
- Projects
- Database
- Computer Science fundamentals

# HR Interview Questions

Generate a few common HR questions suitable for this candidate.

Resume:

{resume_text}
"""

    return ask_ai(prompt)
