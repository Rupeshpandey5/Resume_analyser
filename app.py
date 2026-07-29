import os

from flask import Flask, render_template, request, redirect

from werkzeug.utils import secure_filename

from utils.parser import extract_resume_text
from utils.skills import extract_skills
from utils.analyzer import analyze_resume

from ai.openrouter import get_complete_analysis


UPLOAD_FOLDER = "uploads"


app = Flask(__name__)


app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)



@app.route("/")
def home():

    return render_template(
        "index.html"
    )




@app.route("/analyze", methods=["POST"])
def analyze():


    if "resume" not in request.files:

        return redirect("/")



    file = request.files["resume"]



    if file.filename == "":

        return redirect("/")



    filename = secure_filename(
        file.filename
    )



    filepath = os.path.join(
        UPLOAD_FOLDER,
        filename
    )



    file.save(filepath)



    # Extract resume text
    resume_text = extract_resume_text(filepath)


    print("========== RESUME TEXT ==========")
    print(resume_text)
    print("=================================")



    # Extract skills
    skills = extract_skills(
        resume_text
    )


    print("========== SKILLS ==========")
    print(skills)
    print("============================")



    # Basic resume analysis
    result = analyze_resume(
        resume_text,
        skills
    )



    # Single AI API call
    result["ai_analysis"] = get_complete_analysis(
        resume_text
    )



    return render_template(
        "result.html",
        result=result,
        filename=filename
    )





if __name__ == "__main__":

    app.run(
        debug=True
    )