import os
import requests

from dotenv import load_dotenv

load_dotenv()


API_KEY = os.getenv("OPENROUTER_API_KEY")

URL = "https://openrouter.ai/api/v1/chat/completions"


def ask_ai(prompt):

    if not API_KEY:
        return "AI Error: OpenRouter API key missing."

    try:

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }


        data = {

            "model": "openrouter/free",

            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            "temperature": 0.3

        }


        response = requests.post(
            URL,
            headers=headers,
            json=data,
            timeout=20
        )


        response.raise_for_status()


        result = response.json()


        if "choices" in result:

            return result["choices"][0]["message"]["content"]


        else:

            return "AI Error Response: " + str(result)



    except requests.Timeout:

        return "⚠ AI request timed out. Please try again."


    except requests.RequestException as e:
    if hasattr(e, "response") and e.response is not None:
        return f"⚠ OpenRouter API Error: {e.response.status_code} - {e.response.text}"
    return f"⚠ OpenRouter API Error: {str(e)}"


    except Exception as e:

        return f"⚠ AI Error: {str(e)}"





def get_complete_analysis(resume_text):


    prompt = f"""

You are an expert AI Resume Analyzer and ATS specialist.

Analyze the given resume professionally.

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

Mention strong points of the resume.


# ATS Improvements

Give suggestions to improve ATS score.

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

Generate interview questions based on:
- Programming
- AI/ML
- Projects
- Database
- Computer Science fundamentals


# HR Interview Questions

Generate common HR questions for this candidate.



Resume:

{resume_text}


"""


    return ask_ai(prompt)
