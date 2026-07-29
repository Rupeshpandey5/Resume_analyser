import json


def load_job_skills():

    with open("datasets/job_skills.json", "r") as file:
        data = json.load(file)

    return data["skills"]



def calculate_ats_score(text, skills):

    score = 0

    text_length = len(text)


    # Resume length check
    if text_length > 1000:
        score += 20

    elif text_length > 500:
        score += 15

    else:
        score += 10


    # Skills score
    if len(skills) >= 10:
        score += 30

    elif len(skills) >= 5:
        score += 20

    else:
        score += 10


    # Sections check

    sections = [
        "education",
        "project",
        "experience",
        "skill",
        "certificate"
    ]


    found = 0

    text_lower = text.lower()


    for section in sections:

        if section in text_lower:
            found += 1


    score += found * 5


    # Limit score

    if score > 100:
        score = 100


    return score



def find_missing_skills(skills):

    required = [
        "python",
        "sql",
        "machine learning",
        "git",
        "github",
        "numpy",
        "pandas",
        "scikit-learn",
        "deep learning",
        "docker"
    ]


    missing = []


    for skill in required:

        if skill not in skills:
            missing.append(skill)


    return missing



def resume_strength(score):

    if score >= 80:
        return "Strong Resume"

    elif score >= 50:
        return "Average Resume"

    else:
        return "Needs Improvement"



def recommend_role(skills):

    skills = [s.lower() for s in skills]


    if "machine learning" in skills or "deep learning" in skills:
        return "Machine Learning Engineer"


    elif "python" in skills and "sql" in skills:
        return "Python Developer / Data Analyst"


    elif "html" in skills and "css" in skills:
        return "Frontend Developer"


    elif "java" in skills:
        return "Java Developer"


    else:
        return "Software Engineer"



def generate_suggestions(score, missing):

    suggestions = []


    if score < 70:
        suggestions.append(
            "Improve resume formatting and add more technical details."
        )


    if len(missing) > 0:

        suggestions.append(
            "Add missing skills: " + ", ".join(missing)
        )


    suggestions.append(
        "Add more real-world projects with GitHub links."
    )


    suggestions.append(
        "Use action words like Developed, Designed, Implemented."
    )


    return suggestions



def analyze_resume(text, skills):


    score = calculate_ats_score(
        text,
        skills
    )


    missing = find_missing_skills(
        skills
    )


    result = {

        "ats_score": score,

        "skills": skills,

        "missing_skills": missing,

        "strength": resume_strength(score),

        "role": recommend_role(skills),

        "suggestions": generate_suggestions(
            score,
            missing
        )

    }


    return result