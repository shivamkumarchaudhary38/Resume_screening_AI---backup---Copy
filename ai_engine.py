# ============================================================
# AI ENGINE - FINAL YEAR VERSION
# Offline AI Resume Analyzer
# ============================================================

import re
from typing import List, Dict, Any

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# AI Semantic Model
from sentence_transformers import SentenceTransformer


# ============================================================
# AI SEMANTIC MODEL
# ============================================================

try:

    semantic_model = SentenceTransformer(
        "all-MiniLM-L6-v2"
    )

    SEMANTIC_MODEL_AVAILABLE = True

    print("✓ AI Semantic Model Loaded Successfully")

except Exception as e:

    semantic_model = None

    SEMANTIC_MODEL_AVAILABLE = False

    print(
        "⚠ Semantic model unavailable."
        " Using TF-IDF fallback."
    )


# ============================================================
# 1. TEXT PREPROCESSING
# ============================================================

def clean_text(text: str) -> str:
    """
    Cleans resume and job description text.
    """

    if not text:
        return ""

    text = str(text).lower()

    # Remove email
    text = re.sub(
        r"\b[\w\.-]+@[\w\.-]+\.\w+\b",
        " ",
        text
    )

    # Remove URLs
    text = re.sub(
        r"https?://\S+|www\.\S+",
        " ",
        text
    )

    # Keep useful programming characters
    text = re.sub(
        r"[^a-zA-Z0-9+#.\-/ ]",
        " ",
        text
    )

    # Remove multiple spaces
    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# ============================================================
# 2. TF-IDF SIMILARITY
# ============================================================

def calculate_tfidf_score(
    resume_text: str,
    job_description: str
) -> float:
    """
    Calculates TF-IDF similarity between
    resume and job description.
    """

    resume = clean_text(resume_text)
    job = clean_text(job_description)

    if not resume or not job:
        return 0.0

    try:

        documents = [
            resume,
            job
        ]

        vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2),
            max_features=5000
        )

        matrix = vectorizer.fit_transform(
            documents
        )

        similarity = cosine_similarity(
            matrix[0:1],
            matrix[1:2]
        )[0][0]

        score = similarity * 100

        return round(
            max(0.0, min(score, 100.0)),
            2
        )

    except Exception as e:

        print(
            "TF-IDF Error:",
            e
        )

        return 0.0


# ============================================================
# 3. SEMANTIC AI SIMILARITY
# ============================================================

def calculate_semantic_score(
    resume_text: str,
    job_description: str
) -> float:
    """
    Calculates semantic similarity using
    Sentence Transformer AI model.
    """

    resume = clean_text(resume_text)
    job = clean_text(job_description)

    if not resume or not job:
        return 0.0

    if not SEMANTIC_MODEL_AVAILABLE:

        return 0.0

    try:

        embeddings = semantic_model.encode(
            [resume, job],
            normalize_embeddings=True
        )

        similarity = cosine_similarity(
            [embeddings[0]],
            [embeddings[1]]
        )[0][0]

        # Convert cosine similarity
        # into percentage
        score = similarity * 100

        return round(
            max(0.0, min(score, 100.0)),
            2
        )

    except Exception as e:

        print(
            "Semantic AI Error:",
            e
        )

        return 0.0


# ============================================================
# 4. HYBRID SIMILARITY
# ============================================================

def calculate_similarity(
    resume_text: str,
    job_description: str
) -> float:
    """
    Hybrid AI similarity.

    TF-IDF       = 40%
    Semantic AI  = 60%
    """

    if not resume_text or not job_description:
        return 0.0

    tfidf_score = calculate_tfidf_score(
        resume_text,
        job_description
    )

    semantic_score = calculate_semantic_score(
        resume_text,
        job_description
    )

    # If semantic model is unavailable,
    # use TF-IDF only.
    if SEMANTIC_MODEL_AVAILABLE:

        final_score = (
            tfidf_score * 0.40
            +
            semantic_score * 0.60
        )

    else:

        final_score = tfidf_score

    return round(
        max(0.0, min(final_score, 100.0)),
        2
    )


# ============================================================
# 5. TECHNICAL KEYWORDS
# ============================================================

TECHNICAL_KEYWORDS = [

    "python",
    "java",
    "javascript",
    "typescript",

    "html",
    "css",

    "react",
    "angular",
    "node",
    "node.js",

    "flask",
    "django",
    "fastapi",

    "sql",
    "mysql",
    "postgresql",
    "mongodb",
    "sqlite",

    "git",
    "github",

    "rest",
    "rest api",
    "api",

    "machine learning",
    "deep learning",
    "artificial intelligence",
    "ai",
    "nlp",

    "numpy",
    "pandas",
    "scikit-learn",
    "sklearn",

    "tensorflow",
    "pytorch",
    "opencv",

    "data analysis",
    "data science",

    "power bi",
    "tableau",

    "aws",
    "azure",

    "docker",
    "linux",

    "streamlit",

    "matplotlib",
    "seaborn",

    "flask",
    "web development",

    "computer vision",
    "data visualization",

    "statistics",
    "excel"
]


# ============================================================
# 6. KEYWORD MATCHING
# ============================================================

def find_technical_keywords(
    resume_text: str,
    job_description: str
):

    resume = clean_text(
        resume_text
    )

    job = clean_text(
        job_description
    )

    matched = []
    missing = []

    for keyword in TECHNICAL_KEYWORDS:

        keyword_clean = clean_text(
            keyword
        )

        if keyword_clean in job:

            if keyword_clean in resume:

                matched.append(
                    keyword
                )

            else:

                missing.append(
                    keyword
                )

    return matched, missing


# ============================================================
# 7. EXTRACT KEYWORDS
# ============================================================

def extract_keywords(
    text: str,
    top_n: int = 20
) -> List[str]:
    """
    Extracts important keywords using TF-IDF.
    """

    cleaned = clean_text(
        text
    )

    if not cleaned:
        return []

    try:

        vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2),
            max_features=1000
        )

        matrix = vectorizer.fit_transform(
            [cleaned]
        )

        feature_names = (
            vectorizer.get_feature_names_out()
        )

        scores = matrix.toarray()[0]

        keyword_scores = list(
            zip(
                feature_names,
                scores
            )
        )

        keyword_scores.sort(
            key=lambda x: x[1],
            reverse=True
        )

        keywords = [
            word
            for word, score in keyword_scores[:top_n]
            if score > 0
        ]

        return keywords

    except Exception as e:

        print(
            "Keyword extraction error:",
            e
        )

        return []


# ============================================================
# 8. FIND MATCHED KEYWORDS
# ============================================================

def find_matched_keywords(
    resume_text: str,
    job_description: str,
    top_n: int = 30
) -> List[str]:
    """
    Finds important keywords that occur
    in both resume and job description.
    """

    resume = clean_text(
        resume_text
    )

    job = clean_text(
        job_description
    )

    if not resume or not job:
        return []

    # First check technical keywords
    technical_matched, _ = find_technical_keywords(
        resume,
        job
    )

    # Then TF-IDF keywords
    resume_keywords = set(
        extract_keywords(
            resume,
            top_n
        )
    )

    job_keywords = extract_keywords(
        job,
        top_n
    )

    matched = list(
        technical_matched
    )

    for keyword in job_keywords:

        if keyword in resume_keywords:

            if keyword not in matched:

                matched.append(
                    keyword
                )

    return matched


# ============================================================
# 9. FIND MISSING KEYWORDS
# ============================================================

def find_missing_keywords(
    resume_text: str,
    job_description: str,
    top_n: int = 30
) -> List[str]:
    """
    Finds important keywords required by
    the job but missing from the resume.
    """

    resume = clean_text(
        resume_text
    )

    job = clean_text(
        job_description
    )

    if not job:
        return []

    # Technical missing keywords
    _, technical_missing = find_technical_keywords(
        resume,
        job
    )

    resume_keywords = set(
        extract_keywords(
            resume,
            top_n
        )
    )

    job_keywords = extract_keywords(
        job,
        top_n
    )

    missing = list(
        technical_missing
    )

    for keyword in job_keywords:

        if keyword not in resume_keywords:

            if keyword not in missing:

                missing.append(
                    keyword
                )

    return missing


# ============================================================
# 10. MATCH LEVEL
# ============================================================

def get_match_level(
    score: float
) -> str:
    """
    Converts numerical score into
    human-readable match level.
    """

    if score >= 80:

        return "Excellent Match"

    elif score >= 65:

        return "Strong Match"

    elif score >= 50:

        return "Moderate Match"

    elif score >= 30:

        return "Low Match"

    else:

        return "Very Low Match"


# ============================================================
# 11. COMPLETE HYBRID JOB MATCH
# ============================================================

def hybrid_job_match(
    resume_text: str,
    job_description: str
) -> Dict[str, Any]:
    """
    Complete hybrid AI job matching.

    40% TF-IDF
    60% Semantic AI
    """

    if not resume_text or not job_description:

        return {

            "tfidf_score": 0.0,

            "semantic_score": 0.0,

            "final_score": 0.0,

            "match_score": 0.0,

            "match_level": "No Job Description",

            "matched_keywords": [],

            "missing_keywords": []

        }

    # --------------------------------------------------------
    # TF-IDF
    # --------------------------------------------------------

    tfidf_score = calculate_tfidf_score(
        resume_text,
        job_description
    )

    # --------------------------------------------------------
    # Semantic AI
    # --------------------------------------------------------

    semantic_score = calculate_semantic_score(
        resume_text,
        job_description
    )

    # --------------------------------------------------------
    # Final Hybrid Score
    # --------------------------------------------------------

    if SEMANTIC_MODEL_AVAILABLE:

        final_score = (
            tfidf_score * 0.40
            +
            semantic_score * 0.60
        )

    else:

        final_score = tfidf_score

    final_score = round(
        max(
            0.0,
            min(
                final_score,
                100.0
            )
        ),
        2
    )

    # --------------------------------------------------------
    # Match Level
    # --------------------------------------------------------

    match_level = get_match_level(
        final_score
    )

    # --------------------------------------------------------
    # Keywords
    # --------------------------------------------------------

    matched_keywords = find_matched_keywords(
        resume_text,
        job_description
    )

    missing_keywords = find_missing_keywords(
        resume_text,
        job_description
    )

    # --------------------------------------------------------
    # Result
    # --------------------------------------------------------

    return {

        "tfidf_score": round(
            tfidf_score,
            2
        ),

        "semantic_score": round(
            semantic_score,
            2
        ),

        "final_score": final_score,

        # Compatibility with app.py
        "match_score": final_score,

        "match_level": match_level,

        "matched_keywords":
            matched_keywords,

        "missing_keywords":
            missing_keywords

    }


# ============================================================
# 12. JOB MATCH ANALYSIS
# ============================================================

def analyze_job_match(
    resume_text: str,
    job_description: str
) -> Dict[str, Any]:
    """
    Complete AI job matching analysis.
    """

    if not job_description or not job_description.strip():

        return {

            "match_score": 0.0,

            "match_level":
                "No Job Description",

            "matched_keywords": [],

            "missing_keywords": [],

            "resume_keywords": [],

            "job_keywords": [],

            "tfidf_score": 0.0,

            "semantic_score": 0.0,

            "final_score": 0.0

        }

    hybrid_result = hybrid_job_match(
        resume_text,
        job_description
    )

    resume_keywords = extract_keywords(
        resume_text,
        20
    )

    job_keywords = extract_keywords(
        job_description,
        20
    )

    return {

        "match_score":
            hybrid_result["final_score"],

        "match_level":
            hybrid_result["match_level"],

        "matched_keywords":
            hybrid_result["matched_keywords"],

        "missing_keywords":
            hybrid_result["missing_keywords"],

        "resume_keywords":
            resume_keywords,

        "job_keywords":
            job_keywords,

        "tfidf_score":
            hybrid_result["tfidf_score"],

        "semantic_score":
            hybrid_result["semantic_score"],

        "final_score":
            hybrid_result["final_score"]

    }


# ============================================================
# 13. AI JOB RECOMMENDATIONS
# ============================================================

def generate_job_recommendations(
    match_data: Dict[str, Any]
) -> List[str]:
    """
    Generates recommendations based on
    AI job matching score.
    """

    recommendations = []

    score = match_data.get(
        "match_score",
        0
    )

    missing = match_data.get(
        "missing_keywords",
        []
    )

    matched = match_data.get(
        "matched_keywords",
        []
    )

    # --------------------------------------------------------
    # Score based recommendation
    # --------------------------------------------------------

    if score >= 80:

        recommendations.append(
            "Your resume has excellent alignment "
            "with this job description."
        )

        recommendations.append(
            "Highlight your strongest matching "
            "skills and projects."
        )

    elif score >= 65:

        recommendations.append(
            "Your resume has strong alignment "
            "with this job."
        )

        recommendations.append(
            "Add more job-specific keywords "
            "where relevant."
        )

    elif score >= 50:

        recommendations.append(
            "Your resume has moderate alignment "
            "with this job."
        )

        recommendations.append(
            "Improve the resume by adding "
            "relevant technical skills and projects."
        )

    elif score >= 30:

        recommendations.append(
            "Your resume has limited alignment "
            "with this job."
        )

        recommendations.append(
            "Consider adding relevant skills "
            "and projects if you actually have them."
        )

    else:

        recommendations.append(
            "Your resume has very low alignment "
            "with this job."
        )

        recommendations.append(
            "Review the job requirements and "
            "highlight relevant experience."
        )

    # --------------------------------------------------------
    # Missing keywords
    # --------------------------------------------------------

    if missing:

        important_missing = ", ".join(
            missing[:10]
        )

        recommendations.append(
            "Important missing keywords: "
            + important_missing
        )

    # --------------------------------------------------------
    # Matched keywords
    # --------------------------------------------------------

    if matched:

        important_matched = ", ".join(
            matched[:10]
        )

        recommendations.append(
            "Strong matching keywords: "
            + important_matched
        )

    # --------------------------------------------------------
    # General recommendation
    # --------------------------------------------------------

    recommendations.append(
        "Customize your resume for each job "
        "description instead of using the same "
        "resume for every application."
    )

    return recommendations


# ============================================================
# 14. MAIN AI ANALYSIS FUNCTION
# ============================================================

def run_ai_analysis(
    resume_text: str,
    job_description: str
) -> Dict[str, Any]:
    """
    Main function used by app.py.

    Returns:
    - TF-IDF score
    - Semantic AI score
    - Final hybrid score
    - Match level
    - Matched keywords
    - Missing keywords
    - Recommendations
    """

    # Empty JD check
    if not job_description or not job_description.strip():

        return {

            "match_score": 0.0,

            "tfidf_score": 0.0,

            "semantic_score": 0.0,

            "final_score": 0.0,

            "match_level":
                "No Job Description",

            "matched_keywords": [],

            "missing_keywords": [],

            "resume_keywords": [],

            "job_keywords": [],

            "recommendations": [
                "Please enter a job description "
                "to calculate the AI job match score."
            ]

        }

    # AI matching
    match_data = analyze_job_match(
        resume_text,
        job_description
    )

    # Recommendations
    recommendations = (
        generate_job_recommendations(
            match_data
        )
    )

    # Final result
    result = {

        "match_score":
            match_data["match_score"],

        "tfidf_score":
            match_data["tfidf_score"],

        "semantic_score":
            match_data["semantic_score"],

        "final_score":
            match_data["final_score"],

        "match_level":
            match_data["match_level"],

        "matched_keywords":
            match_data["matched_keywords"],

        "missing_keywords":
            match_data["missing_keywords"],

        "resume_keywords":
            match_data["resume_keywords"],

        "job_keywords":
            match_data["job_keywords"],

        "recommendations":
            recommendations

    }

    return result


# ============================================================
# 15. TEST MODE
# ============================================================

if __name__ == "__main__":

    test_resume = """
    Python developer with experience in Flask,
    SQL, MySQL, Git, GitHub, HTML, CSS
    and JavaScript.

    Developed web applications using Python
    and Flask.

    Knowledge of Machine Learning,
    Data Analysis and REST API.
    """

    test_job = """
    We are looking for a Python Developer
    with experience in Python, Flask, SQL,
    Git, REST API and Machine Learning.

    The candidate should have knowledge of
    web development, HTML, CSS and JavaScript.
    """

    result = run_ai_analysis(
        test_resume,
        test_job
    )

    print("\n")
    print("=" * 60)
    print("AI RESUME VS JOB DESCRIPTION MATCH")
    print("=" * 60)

    print(
        "\nTF-IDF Score:",
        result["tfidf_score"],
        "%"
    )

    print(
        "Semantic AI Score:",
        result["semantic_score"],
        "%"
    )

    print(
        "Final Hybrid Score:",
        result["final_score"],
        "%"
    )

    print(
        "Match Score:",
        result["match_score"],
        "%"
    )

    print(
        "Match Level:",
        result["match_level"]
    )

    print("\nMatched Keywords:")

    if result["matched_keywords"]:

        for keyword in result["matched_keywords"]:

            print(
                "✓",
                keyword
            )

    else:

        print(
            "No matched keywords found."
        )

    print("\nMissing Keywords:")

    if result["missing_keywords"]:

        for keyword in result["missing_keywords"]:

            print(
                "✗",
                keyword
            )

    else:

        print(
            "No major missing keywords found."
        )

    print("\nAI Recommendations:")

    for recommendation in result["recommendations"]:

        print(
            "→",
            recommendation
        )

    print("\n")
    print("=" * 60)
    print("TEST COMPLETED")
    print("=" * 60)