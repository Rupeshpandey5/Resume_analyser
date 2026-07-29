import os
import requests

from dotenv import load_dotenv


load_dotenv()


API_KEY = os.getenv(
    "OPENROUTER_API_KEY"
)


URL = "https://openrouter.ai/api/v1/chat/completions"



def ask_ai(prompt):

    try:

        headers = {

            "Authorization": f"Bearer {API_KEY}",

            "Content-Type": "application/json"

        }


        data = {
    "model": "inclusionai/ling-3.0-flash:free",
    "messages": [
        {
            "role": "user",
            "content": prompt
        }
    ]
}


        response = requests.post(

            URL,

            headers=headers,

            json=data

        )


        result = response.json()


        if "choices" in result:

            return result["choices"][0]["message"]["content"]


        return str(result)



    except Exception as e:

        return "AI Error: " + str(e)





def get_resume_summary(resume_text):


    prompt = f"""

You are an AI Resume Analyzer.

Analyze this resume.

Give:

1. Candidate Summary
2. Technical Skills
3. Strengths
4. Weaknesses
5. Suitable Job Roles


Resume:

{resume_text}

"""


    return ask_ai(prompt)






def get_resume_improvement(resume_text):


    prompt = f"""

You are a professional resume expert.

Review this resume and provide improvement suggestions.

Focus on:

- ATS score improvement
- Skills
- Projects
- Formatting
- Missing information


Resume:

{resume_text}

"""


    return ask_ai(prompt)







def get_interview_questions(resume_text):


    prompt = f"""

Generate interview questions from this resume.

Include:

Technical Questions:
- Python
- AI/ML
- Projects
- Database

HR Questions:


Resume:

{resume_text}

"""


    return ask_ai(prompt)