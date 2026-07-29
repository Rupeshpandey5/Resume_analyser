import json


def load_skills():

    with open("datasets/job_skills.json", "r") as file:

        data = json.load(file)

    return data["skills"]


def extract_skills(resume_text):

    resume_text = resume_text.lower()

    skills = []

    database = load_skills()

    for skill in database:

        if skill.lower() in resume_text:
            skills.append(skill)

    return sorted(list(set(skills)))