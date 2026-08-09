from flask import Flask, render_template, request, send_file
import os
import re
from datetime import datetime

from resume_parser import (
    extract_text,
    extract_skills,
    extract_education,
    extract_experience,
    calculate_score,
    offline_ai_review,
    skill_gap_analysis
)

from report_generator import generate_report


app = Flask(__name__)

# =======================================================
# FOLDERS
# =======================================================

UPLOAD_FOLDER = "uploads"
REPORT_FOLDER = "reports"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(REPORT_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# =======================================================
# HOME PAGE
# =======================================================

@app.route("/")
def index():
    return render_template("index.html")


# =======================================================
# TEXT NORMALIZATION
# =======================================================

def normalize_text(text):
    """
    Convert text into a clean searchable format.
    """

    if not text:
        return ""

    text = str(text).lower()

    # Replace common separators with spaces
    text = text.replace("/", " ")
    text = text.replace("-", " ")
    text = text.replace("_", " ")

    # Remove punctuation
    text = re.sub(r"[^a-z0-9+#.\s]", " ", text)

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# =======================================================
# SKILL MATCHING
# =======================================================

def calculate_skill_match(resume_text, required_skills):
    """
    Calculate job match based mainly on required skills.

    Returns:
        score
        matched_skills
        missing_skills
    """

    if not required_skills:
        return 0.0, [], []

    resume_clean = normalize_text(resume_text)

    matched = []
    missing = []

    for skill in required_skills:

        skill_clean = normalize_text(skill)

        if not skill_clean:
            continue

        # Exact phrase matching
        if skill_clean in resume_clean:
            matched.append(skill)
        else:
            missing.append(skill)

    # Remove duplicates
    matched = sorted(
        set(matched),
        key=lambda x: str(x).lower()
    )

    missing = sorted(
        set(missing),
        key=lambda x: str(x).lower()
    )

    total = len(matched) + len(missing)

    if total == 0:
        score = 0
    else:
        score = (len(matched) / total) * 100

    return round(score, 2), matched, missing


# =======================================================
# KEYWORD MATCHING
# =======================================================

def calculate_keyword_match(resume_text, job_description):
    """
    Calculate cleaned keyword overlap.
    """

    resume_clean = normalize_text(resume_text)
    job_clean = normalize_text(job_description)

    if not resume_clean or not job_clean:
        return 0.0, [], []

    resume_words = set(
        word
        for word in resume_clean.split()
        if len(word) > 2
    )

    job_words = set(
        word
        for word in job_clean.split()
        if len(word) > 2
    )

    if not job_words:
        return 0.0, [], []

    matched_words = sorted(
        resume_words.intersection(job_words)
    )

    missing_words = sorted(
        job_words.difference(resume_words)
    )

    score = (
        len(matched_words)
        / len(job_words)
    ) * 100

    return round(
        min(score, 100),
        2
    ), matched_words, missing_words


# =======================================================
# RESUME ANALYSIS
# =======================================================

@app.route("/analyze", methods=["POST"])
@app.route("/upload", methods=["POST"])
def analyze():

    # ===================================================
    # RESUME FILE
    # ===================================================

    resume_file = request.files.get("resume")

    # ===================================================
    # JOB DESCRIPTION
    # ===================================================

    job_description = request.form.get(
        "job_description",
        ""
    ).strip()

    # ===================================================
    # CHECK RESUME
    # ===================================================

    if not resume_file:
        return "Please upload a resume."

    if resume_file.filename == "":
        return "Please select a resume file."

    # ===================================================
    # SAVE RESUME
    # ===================================================

    resume_path = os.path.join(
        UPLOAD_FOLDER,
        resume_file.filename
    )

    resume_file.save(resume_path)

    # ===================================================
    # EXTRACT RESUME TEXT
    # ===================================================

    resume_text = extract_text(resume_path)

    if not resume_text:
        return "Unable to extract text from the resume."

    # ===================================================
    # EXTRACT RESUME INFORMATION
    # ===================================================

    skills = extract_skills(resume_text)

    education = extract_education(resume_text)

    experience = extract_experience(resume_text)

    # ===================================================
    # RESUME SCORE
    # ===================================================

    score = calculate_score(
        resume_text,
        skills,
        education,
        experience
    )

    # ===================================================
    # OFFLINE AI REVIEW
    # ===================================================

    ai_review = offline_ai_review(
        resume_text,
        skills,
        education,
        experience,
        score
    )

    # ===================================================
    # SKILL GAP ANALYSIS
    # ===================================================

    try:

        skill_gap = skill_gap_analysis(
            resume_text,
            job_description
        )

    except Exception as e:

        print(
            "Skill Gap Analysis Error:",
            e
        )

        skill_gap = (
            skills,
            [],
            []
        )

    # Make sure skill_gap has 3 values

    if not isinstance(skill_gap, (list, tuple)):

        skill_gap = (
            skills,
            [],
            []
        )

    while len(skill_gap) < 3:

        skill_gap = tuple(skill_gap) + ([],)

    resume_skills_gap = skill_gap[0] or []
    required_skills = skill_gap[1] or []
    missing_skills = skill_gap[2] or []

    # ===================================================
    # JOB MATCHING
    # ===================================================

    # ---------------------------------------------------
    # 1. SKILL MATCH SCORE
    # ---------------------------------------------------

    skill_match_score, matched_skill_list, missing_skill_list = (
        calculate_skill_match(
            resume_text,
            required_skills
        )
    )

    # ---------------------------------------------------
    # 2. KEYWORD MATCH SCORE
    # ---------------------------------------------------

    keyword_match_score, matched_words, missing_words = (
        calculate_keyword_match(
            resume_text,
            job_description
        )
    )

    # ===================================================
    # AI JOB MATCHING
    # ===================================================

    ai_match_result = {}

    try:

        from ai_engine import run_ai_analysis

        ai_match_result = run_ai_analysis(
            resume_text,
            job_description
        )

        if not isinstance(
            ai_match_result,
            dict
        ):

            ai_match_result = {}

    except Exception as e:

        print(
            "AI Job Matching Error:",
            e
        )

        ai_match_result = {}

    # ===================================================
    # AI MATCH SCORE
    # ===================================================

    ai_score = ai_match_result.get(
        "match_score",
        None
    )

    if ai_score is None:

        ai_score = ai_match_result.get(
            "final_score",
            None
        )

    try:

        if ai_score is not None:

            ai_score = float(ai_score)

            ai_score = round(
                max(
                    0,
                    min(
                        ai_score,
                        100
                    )
                ),
                2
            )

        else:

            ai_score = None

    except (
        TypeError,
        ValueError
    ):

        ai_score = None

    # ===================================================
    # FINAL JOB MATCH SCORE
    # ===================================================

    if required_skills:

        # Skill matching gets highest importance
        #
        # 70% = required skill matching
        # 20% = keyword matching
        # 10% = AI score (if available)

        if ai_score is not None:

            hybrid_score = (
                (skill_match_score * 0.70)
                +
                (keyword_match_score * 0.20)
                +
                (ai_score * 0.10)
            )

        else:

            hybrid_score = (
                (skill_match_score * 0.80)
                +
                (keyword_match_score * 0.20)
            )

    else:

        # If no skills are detected in JD,
        # use keyword matching.

        if ai_score is not None:

            hybrid_score = (
                (keyword_match_score * 0.70)
                +
                (ai_score * 0.30)
            )

        else:

            hybrid_score = keyword_match_score

    # Keep score between 0 and 100

    hybrid_score = round(
        max(
            0,
            min(
                hybrid_score,
                100
            )
        ),
        2
    )

    # ===================================================
    # MATCH LEVEL
    # ===================================================

    if hybrid_score >= 80:

        hybrid_match_level = "Excellent Match"

    elif hybrid_score >= 65:

        hybrid_match_level = "Strong Match"

    elif hybrid_score >= 50:

        hybrid_match_level = "Moderate Match"

    elif hybrid_score >= 35:

        hybrid_match_level = "Low Match"

    else:

        hybrid_match_level = "Very Low Match"

    # ===================================================
    # FINAL MATCH SCORE VARIABLE
    # ===================================================

    match_score = hybrid_score

    # ===================================================
    # TF-IDF SCORE
    # ===================================================

    tfidf_score = ai_match_result.get(
        "tfidf_score",
        0
    )

    try:

        tfidf_score = float(
            tfidf_score
        )

    except (
        TypeError,
        ValueError
    ):

        tfidf_score = 0

    # ===================================================
    # SEMANTIC SCORE
    # ===================================================

    semantic_score = ai_match_result.get(
        "semantic_score",
        0
    )

    try:

        semantic_score = float(
            semantic_score
        )

    except (
        TypeError,
        ValueError
    ):

        semantic_score = 0

    # ===================================================
    # MATCHED KEYWORDS
    # ===================================================

    matched_keywords = ai_match_result.get(
        "matched_keywords",
        []
    )

    if not matched_keywords:

        matched_keywords = matched_skill_list

    if not matched_keywords:

        matched_keywords = matched_words

    matched_keywords = [
        str(word)
        for word in matched_keywords
        if len(str(word).strip()) > 2
    ]

    matched_keywords = sorted(
        set(matched_keywords),
        key=lambda x: x.lower()
    )

    # ===================================================
    # MISSING KEYWORDS
    # ===================================================

    missing_keywords = ai_match_result.get(
        "missing_keywords",
        []
    )

    if not missing_keywords:

        missing_keywords = missing_skill_list

    if not missing_keywords:

        missing_keywords = missing_words

    missing_keywords = [
        str(word)
        for word in missing_keywords
        if len(str(word).strip()) > 2
    ]

    missing_keywords = sorted(
        set(missing_keywords),
        key=lambda x: x.lower()
    )

    # ===================================================
    # RECOMMENDATIONS
    # ===================================================

    recommendations = []

    if hybrid_score < 50:

        recommendations.append(
            "Your resume has limited alignment with this job."
        )

        recommendations.append(
            "Add relevant skills from the job description where you have actual knowledge or experience."
        )

    elif hybrid_score < 65:

        recommendations.append(
            "Your resume has moderate alignment with this job."
        )

        recommendations.append(
            "Add more job-specific skills and keywords where relevant."
        )

    elif hybrid_score < 80:

        recommendations.append(
            "Your resume has strong alignment with this job."
        )

        recommendations.append(
            "Add missing skills where you have relevant knowledge or project experience."
        )

    else:

        recommendations.append(
            "Your resume has excellent alignment with this job."
        )

        recommendations.append(
            "Keep the resume customized for this job."
        )

    # ---------------------------------------------------
    # Missing skills recommendation
    # ---------------------------------------------------

    if missing_skill_list:

        recommendations.append(
            "Important missing skills: "
            + ", ".join(
                missing_skill_list[:15]
            )
        )

    # ===================================================
    # GENERATE PDF REPORT
    # ===================================================

    report_path = os.path.join(
        REPORT_FOLDER,
        "Resume_Report.pdf"
    )

    try:

        generate_report(
            report_path,
            score,
            skills,
            education,
            experience,
            ai_review,
            hybrid_score
        )

    except Exception as e:

        print(
            "Report generation error:",
            e
        )

    # ===================================================
    # HTML DATA
    # ===================================================

    skills_html = (
        "<br>".join(
            skills
        )
        if skills
        else "Not Found"
    )

    education_html = (
        "<br>".join(
            education
        )
        if education
        else "Not Found"
    )

    experience_html = (
        experience.replace(
            "\n",
            "<br>"
        )
        if experience
        else "Not Found"
    )

    review_html = (
        ai_review.replace(
            "\n",
            "<br>"
        )
        if ai_review
        else "No AI review available."
    )

    # ===================================================
    # RESUME QUALITY
    # ===================================================

    if score >= 80:

        quality = "⭐⭐⭐⭐⭐ Excellent Resume"
        quality_color = "green"

    elif score >= 60:

        quality = "⭐⭐⭐⭐ Good Resume"
        quality_color = "darkgoldenrod"

    elif score >= 40:

        quality = "⭐⭐⭐ Average Resume"
        quality_color = "orange"

    else:

        quality = "⭐⭐ Needs Improvement"
        quality_color = "red"

    # ===================================================
    # DATE AND TIME
    # ===================================================

    analysis_date = datetime.now().strftime(
        "%d-%m-%Y %H:%M:%S"
    )

    # ===================================================
    # RESULT DASHBOARD
    # ===================================================

    return render_template(

        "result.html",

        filename=resume_file.filename,

        # Resume score
        score=score,

        quality=quality,

        quality_color=quality_color,

        # Job match
        match_score=match_score,

        hybrid_score=hybrid_score,

        hybrid_match_level=hybrid_match_level,

        # AI scores
        ai_score=ai_score if ai_score is not None else 0,

        tfidf_score=tfidf_score,

        semantic_score=semantic_score,

        # Keywords
        matched_keywords=matched_keywords,

        missing_keywords=missing_keywords,

        # Skill gap
        resume_skills=resume_skills_gap,

        required_skills=required_skills,

        missing_skills=(
            missing_skill_list
            if missing_skill_list
            else missing_skills
        ),

        # Resume information
        skills=skills,

        skills_html=skills_html,

        education=education,

        education_html=education_html,

        experience=experience,

        experience_html=experience_html,

        # AI review
        review=ai_review,

        review_html=review_html,

        # Recommendations
        recommendations=recommendations,

        # Resume text
        text=resume_text,

        # Date
        analysis_date=analysis_date
    )


# =======================================================
# DOWNLOAD PDF REPORT
# =======================================================

@app.route("/download")
def download():

    report_path = os.path.join(
        REPORT_FOLDER,
        "Resume_Report.pdf"
    )

    if os.path.exists(report_path):

        return send_file(
            report_path,
            as_attachment=True,
            download_name="Resume_Report.pdf",
            mimetype="application/pdf"
        )

    return """
    <h2>PDF Report Not Found</h2>
    <br>
    <a href="/">⬅ Back to Home</a>
    """


# =======================================================
# RUN FLASK APPLICATION
# =======================================================

if __name__ == "__main__":

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )