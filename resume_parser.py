import fitz
import re

# ==========================================
# VERSION 3.1
# SMART SKILL NORMALIZATION ENGINE
# ==========================================

# ==========================================
# VERSION 4.0
# SMART SKILL NORMALIZATION ENGINE
# ==========================================

SKILL_ALIASES = {

    # -----------------------------
    # Programming Languages
    # -----------------------------
    "python": "Python",
    "python3": "Python",

    "javascript": "JavaScript",
    "java script": "JavaScript",
    "js": "JavaScript",

    "typescript": "TypeScript",

    "java": "Java",

    "c++": "C++",
    "cpp": "C++",

    "c#": "C#",
    "csharp": "C#",

    "php": "PHP",
    "go": "Go",
    "kotlin": "Kotlin",
    "swift": "Swift",
    "rust": "Rust",

    # -----------------------------
    # Frontend
    # -----------------------------
    "html": "HTML",
    "html5": "HTML",

    "css": "CSS",
    "css3": "CSS",

    "bootstrap": "Bootstrap",

    "tailwind": "Tailwind CSS",
    "tailwind css": "Tailwind CSS",

    "react": "React",
    "react js": "React",

    "angular": "Angular",
    "vue": "Vue",
    "jquery": "jQuery",

    # -----------------------------
    # Backend
    # -----------------------------
    "node.js": "Node.js",
    "nodejs": "Node.js",
    "node js": "Node.js",

    "express": "Express",

    "flask": "Flask",
    "django": "Django",
    "fastapi": "FastAPI",

    "spring boot": "Spring Boot",

    # -----------------------------
    # Database
    # -----------------------------
    "sql": "SQL",
    "mysql": "MySQL",
    "postgresql": "PostgreSQL",
    "postgres": "PostgreSQL",
    "mongodb": "MongoDB",
    "sqlite": "SQLite",
    "oracle": "Oracle",
    "firebase": "Firebase",

    # -----------------------------
    # AI / Machine Learning
    # -----------------------------
    "artificial intelligence": "Artificial Intelligence",
    "ai": "Artificial Intelligence",

    "machine learning": "Machine Learning",
    "ml": "Machine Learning",

    "deep learning": "Deep Learning",

    "data science": "Data Science",
    "data analysis": "Data Analysis",

    "natural language processing": "NLP",
    "nlp": "NLP",

    "computer vision": "Computer Vision",

    "generative ai": "Generative AI",
    "generative artificial intelligence": "Generative AI",

    "llm": "LLM",
    "large language model": "LLM",

    "chatgpt": "ChatGPT",

    # -----------------------------
    # Python Libraries
    # -----------------------------
    "numpy": "NumPy",
    "pandas": "Pandas",
    "matplotlib": "Matplotlib",

    "opencv": "OpenCV",
    "opencv-python": "OpenCV",

    "scikit-learn": "Scikit-Learn",
    "scikit learn": "Scikit-Learn",
    "sklearn": "Scikit-Learn",

    "tensorflow": "TensorFlow",
    "keras": "Keras",

    "streamlit": "Streamlit",

    # -----------------------------
    # Cloud
    # -----------------------------
    "aws": "AWS",
    "amazon web services": "AWS",

    "azure": "Azure",
    "microsoft azure": "Azure",

    "gcp": "GCP",
    "google cloud": "GCP",

    # -----------------------------
    # Tools
    # -----------------------------
    "git": "Git",
    "github": "GitHub",

    "linux": "Linux",
    "windows": "Windows",

    "vs code": "VS Code",
    "visual studio code": "VS Code",

    "excel": "Microsoft Excel",
    "microsoft excel": "Microsoft Excel",

    "power bi": "Power BI",
    "tableau": "Tableau",

    # -----------------------------
    # Soft Skills
    # -----------------------------
    "communication": "Communication",
    "communication skills": "Communication",

    "leadership": "Leadership",
    "teamwork": "Teamwork",

    "problem solving": "Problem Solving",
    "problem-solving": "Problem Solving",

    "critical thinking": "Critical Thinking",
    "analytical thinking": "Analytical Thinking",

    "time management": "Time Management",

    "presentation": "Presentation",
    "presentation skills": "Presentation"
}


# ==========================================
# NORMALIZE SINGLE SKILL
# ==========================================

def normalize_skill(skill):

    if not skill:
        return None

    skill = str(skill).strip()

    # Remove unnecessary punctuation
    key = skill.lower().strip()

    key = key.replace("_", " ")
    key = re.sub(r"\s+", " ", key)

    # Normalize hyphen variations
    key = key.replace("–", "-")
    key = key.replace("—", "-")

    # Check aliases
    if key in SKILL_ALIASES:
        return SKILL_ALIASES[key]

    # Unknown skill:
    # Keep original formatting but clean spaces
    return skill.strip()


# ==========================================
# CLEAN AND DEDUPLICATE SKILLS
# ==========================================

def clean_skills(skills):

    if not skills:
        return []

    cleaned = []
    seen = set()

    for skill in skills:

        normalized = normalize_skill(skill)

        if not normalized:
            continue

        duplicate_key = normalized.lower().strip()

        if duplicate_key not in seen:

            seen.add(duplicate_key)

            cleaned.append(normalized)

    # Sort alphabetically
    return sorted(cleaned, key=lambda x: x.lower())
# ----------------------------------
# Extract Text From PDF
# ----------------------------------

def extract_text(pdf_path):

    text = ""

    try:

        doc = fitz.open(pdf_path)

        for page in doc:
            text += page.get_text()

        doc.close()

    except Exception:
        text = ""

    return text


# ----------------------------------
# Skills Database (Version 3.0)
# ----------------------------------

SKILLS_DB = [

    # Programming Languages
    "python",
    "java",
    "c",
    "c++",
    "c#",
    "javascript",
    "typescript",
    "php",
    "go",
    "kotlin",
    "swift",
    "rust",

    # Frontend
    "html",
    "html5",
    "css",
    "css3",
    "bootstrap",
    "tailwind css",
    "tailwind",
    "react",
    "react js",
    "angular",
    "vue",
    "jquery",

    # Backend
    "node.js",
    "nodejs",
    "express",
    "flask",
    "django",
    "fastapi",
    "spring boot",

    # Database
    "sql",
    "mysql",
    "postgresql",
    "mongodb",
    "sqlite",
    "oracle",
    "firebase",

    # AI / ML
    "artificial intelligence",
    "machine learning",
    "deep learning",
    "data science",
    "data analysis",
    "nlp",
    "computer vision",
    "generative ai",
    "llm",
    "chatgpt",

    # Python Libraries
    "numpy",
    "pandas",
    "matplotlib",
    "opencv",
    "scikit-learn",
    "tensorflow",
    "keras",
    "streamlit",

    # Cloud
    "aws",
    "azure",
    "gcp",

    # Tools
    "git",
    "github",
    "linux",
    "windows",
    "vs code",
    "visual studio code",
    "excel",
    "power bi",
    "tableau",

    # Soft Skills
    "communication",
    "leadership",
    "teamwork",
    "problem solving",
    "critical thinking",
    "time management",
    "presentation",
    "analytical thinking"
]
# ----------------------------------
# Extract Skills (Version 4.0)
# ----------------------------------

def extract_skills(text):

    if not text:
        return []

    text = text.lower()

    found_skills = []

    # ----------------------------------
    # Normalize Resume Text
    # ----------------------------------

    normalized_text = re.sub(
        r"[^a-zA-Z0-9+#.\- ]",
        " ",
        text
    )

    normalized_text = re.sub(
        r"\s+",
        " ",
        normalized_text
    ).strip()

    # ----------------------------------
    # Search Skills From Database
    # ----------------------------------

    for skill in SKILLS_DB:

        skill_lower = skill.lower()

        # Special handling for skills containing
        # punctuation such as C++, C#, Node.js
        if skill_lower in [
            "c++",
            "c#",
            "node.js"
        ]:

            pattern = re.escape(skill_lower)

        else:

            pattern = r"(?<!\w)" + re.escape(skill_lower) + r"(?!\w)"

        if re.search(pattern, normalized_text):

            normalized_skill = normalize_skill(skill)

            if normalized_skill:
                found_skills.append(normalized_skill)

    # ----------------------------------
    # Additional Skill Variations
    # ----------------------------------

    variation_patterns = {

        "html5": "HTML",
        "html 5": "HTML",

        "css3": "CSS",
        "css 3": "CSS",

        "javascript": "JavaScript",
        "java script": "JavaScript",

        "node js": "Node.js",
        "nodejs": "Node.js",
        "node.js": "Node.js",

        "react js": "React",
        "reactjs": "React",

        "tailwind css": "Tailwind CSS",

        "visual studio code": "VS Code",
        "vs code": "VS Code",

        "power bi": "Power BI",

        "machine learning": "Machine Learning",

        "deep learning": "Deep Learning",

        "artificial intelligence": "Artificial Intelligence",

        "generative ai": "Generative AI",

        "data analysis": "Data Analysis"
    }

    for variation, standard_skill in variation_patterns.items():

        if variation in normalized_text:

            found_skills.append(standard_skill)

    # ----------------------------------
    # Final Normalization + Deduplication
    # ----------------------------------

    return clean_skills(found_skills)
# ----------------------------------
# Extract Email
# ----------------------------------

def extract_email(text):

    pattern = r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}'

    result = re.findall(pattern, text)

    if result:
        return result[0]

    return "Not Found"


# ----------------------------------
# Extract Phone Number
# ----------------------------------

def extract_phone(text):

    pattern = r'(\+91[\-\s]?)?[6-9]\d{9}'

    result = re.findall(pattern, text)

    if result:

        if isinstance(result[0], tuple):
            return "".join(result[0])

        return result[0]

    return "Not Found"


# ----------------------------------
# Extract LinkedIn Profile
# ----------------------------------

def extract_linkedin(text):

    pattern = r'(https?://)?(www\.)?linkedin\.com/[^\s]+'

    result = re.findall(pattern, text)

    if "linkedin.com" in text.lower():
        return "Found"

    return "Not Found"


# ----------------------------------
# Extract GitHub Profile
# ----------------------------------

def extract_github(text):

    pattern = r'(https?://)?(www\.)?github\.com/[^\s]+'

    result = re.findall(pattern, text)

    if "github.com" in text.lower():
        return "Found"

    return "Not Found"
# ----------------------------------
# Extract Education
# ----------------------------------

def extract_education(text):

    text = text.lower()

    education = []

    keywords = [

        "10th",
        "12th",

        "high school",
        "intermediate",

        "iti",

        "diploma",

        "b.tech",
        "btech",
        "b.e",
        "be",

        "bca",
        "mca",

        "b.sc",
        "m.sc",

        "b.com",
        "m.com",

        "mba",

        "phd"

    ]

    for item in keywords:

        if item in text:

            education.append(item.upper())

    return sorted(list(set(education)))


# ----------------------------------
# Extract Experience
# ----------------------------------

def extract_experience(text):

    text = text.lower()

    pattern = r'(\d+)\s*(year|years|yr|yrs)'

    result = re.findall(pattern, text)

    if result:

        return result[0][0] + " Years"

    return "Fresher"

# ----------------------------------
# Calculate ATS Score (Version 3.0)
# ----------------------------------

def calculate_score(
    text,
    skills,
    education,
    experience
):

    score = 0

    text_lower = text.lower()

    # ----------------------------------
    # Resume Length (20 Marks)
    # ----------------------------------

    word_count = len(text.split())

    if word_count >= 350:
        score += 20
    elif word_count >= 250:
        score += 16
    elif word_count >= 150:
        score += 12
    elif word_count >= 80:
        score += 8

    # ----------------------------------
    # Skills (30 Marks)
    # ----------------------------------

    skill_count = len(skills)

    if skill_count >= 12:
        score += 30
    elif skill_count >= 10:
        score += 26
    elif skill_count >= 8:
        score += 22
    elif skill_count >= 6:
        score += 18
    elif skill_count >= 4:
        score += 12
    elif skill_count >= 2:
        score += 8

    # ----------------------------------
    # Education (15 Marks)
    # ----------------------------------

    if education:
        score += 15

    # ----------------------------------
    # Experience (15 Marks)
    # ----------------------------------

    if experience and experience.lower() != "not found":
        score += 15

    # ----------------------------------
    # Projects (10 Marks)
    # ----------------------------------

    if any(word in text_lower for word in [
        "project",
        "projects",
        "developed",
        "built",
        "created"
    ]):
        score += 10

    # ----------------------------------
    # Certifications (5 Marks)
    # ----------------------------------

    if any(word in text_lower for word in [
        "certificate",
        "certification",
        "certifications"
    ]):
        score += 5

    # ----------------------------------
    # GitHub / LinkedIn (5 Marks)
    # ----------------------------------

    if "github" in text_lower:
        score += 3

    if "linkedin" in text_lower:
        score += 2

    # ----------------------------------
    # Maximum Score = 100
    # ----------------------------------

    return min(score, 100)
# ----------------------------------
# Offline AI Resume Review (Version 3.0)
# ----------------------------------

def offline_ai_review(
    text,
    skills,
    education,
    experience,
    score
):

    review = []

    review.append("===== AI RESUME ANALYSIS REPORT =====\n")

    # ----------------------------------
    # ATS Score Analysis
    # ----------------------------------

    review.append(f"ATS Score : {score}/100\n")

    if score >= 85:

        review.append(
            "Excellent ATS Score. Your resume is highly ATS-friendly.\n"
        )

    elif score >= 70:

        review.append(
            "Good ATS Score. A few improvements can make it stronger.\n"
        )

    elif score >= 50:

        review.append(
            "Average ATS Score. Improve skills and resume sections.\n"
        )

    else:

        review.append(
            "Low ATS Score. Resume needs significant improvements.\n"
        )

    # ----------------------------------
    # Skills
    # ----------------------------------

    review.append("\n===== SKILLS ANALYSIS =====\n")

    if skills:

        review.append(
            f"Technical Skills Found ({len(skills)}):\n"
        )

        review.append(
            ", ".join(skills)
        )

        review.append("\n")

    else:

        review.append(
            "No technical skills detected.\n"
        )

    # ----------------------------------
    # Education
    # ----------------------------------

    review.append("\n===== EDUCATION =====\n")

    if education:

        review.append(
            "Education details detected.\n"
        )

    else:

        review.append(
            "Education section not detected.\n"
        )

    # ----------------------------------
    # Experience
    # ----------------------------------

    review.append("\n===== EXPERIENCE =====\n")

    if experience and experience.lower() != "not found":

        review.append(
            "Experience section detected.\n"
        )

    else:

        review.append(
            "No experience mentioned.\n"
        )

    # ----------------------------------
    # Projects
    # ----------------------------------

    review.append("\n===== PROJECTS =====\n")

    project_keywords = [
        "project",
        "developed",
        "created",
        "built"
    ]

    if any(
        keyword in text.lower()
        for keyword in project_keywords
    ):

        review.append(
            "Projects section detected.\n"
        )

    else:

        review.append(
            "Add 2-3 academic or personal projects.\n"
        )

    # ----------------------------------
    # Certifications
    # ----------------------------------

    review.append("\n===== CERTIFICATIONS =====\n")

    if any(
        word in text.lower()
        for word in [
            "certificate",
            "certification"
        ]
    ):

        review.append(
            "Certifications detected.\n"
        )

    else:

        review.append(
            "Add relevant certifications (IBM, Python, SQL, AI).\n"
        )

    # ----------------------------------
    # Suggestions
    # ----------------------------------

    review.append("\n===== IMPROVEMENT SUGGESTIONS =====\n")

    if len(skills) < 6:

        review.append(
            "- Add more technical skills.\n"
        )

    if "github" not in text.lower():

        review.append(
            "- Add GitHub profile.\n"
        )

    if "linkedin" not in text.lower():

        review.append(
            "- Add LinkedIn profile.\n"
        )

    if "internship" not in text.lower():

        review.append(
            "- Mention internships if available.\n"
        )

    if "achievement" not in text.lower():

        review.append(
            "- Add achievements or accomplishments.\n"
        )

    review.append(
        "- Keep resume to 1 page.\n"
    )

    review.append(
        "- Use action verbs like Developed, Designed, Built.\n"
    )

    review.append(
        "- Save resume in PDF format.\n"
    )

    review.append(
        "\nOverall Resume Evaluation Completed Successfully."
    )

    return "".join(review)

# ----------------------------------
# SMART SKILL GAP ANALYSIS
# Version 5.0
# ----------------------------------

def skill_gap_analysis(resume_text, job_description):

    # ----------------------------------
    # Extract Resume Skills
    # ----------------------------------

    resume_skills = clean_skills(
        extract_skills(resume_text)
    )

    # ----------------------------------
    # If JD is Empty
    # ----------------------------------

    if not job_description or not job_description.strip():
        return (
            resume_skills,
            [],
            []
        )

    # ----------------------------------
    # Normalize Resume Skills
    # ----------------------------------

    resume_skill_map = {}

    for skill in resume_skills:

        normalized = normalize_skill(skill)

        if normalized:
            resume_skill_map[normalized.lower()] = normalized

    # ----------------------------------
    # Normalize Job Description
    # ----------------------------------

    jd_text = job_description.lower()

    jd_text = jd_text.replace("–", "-")
    jd_text = jd_text.replace("—", "-")

    jd_text = re.sub(
        r"[^a-zA-Z0-9+#.\- ]",
        " ",
        jd_text
    )

    jd_text = re.sub(
        r"\s+",
        " ",
        jd_text
    ).strip()

    # ----------------------------------
    # JD Skill Aliases
    # ----------------------------------

    jd_skill_aliases = {

        # Programming
        "python": "Python",
        "python 3": "Python",
        "python3": "Python",

        "javascript": "JavaScript",
        "java script": "JavaScript",
        "js": "JavaScript",

        "typescript": "TypeScript",

        "java": "Java",

        "c++": "C++",
        "cpp": "C++",

        "c#": "C#",
        "c sharp": "C#",

        # Frontend
        "html": "HTML",
        "html5": "HTML",
        "html 5": "HTML",

        "css": "CSS",
        "css3": "CSS",
        "css 3": "CSS",

        "bootstrap": "Bootstrap",

        "tailwind": "Tailwind CSS",
        "tailwind css": "Tailwind CSS",

        "react": "React",
        "reactjs": "React",
        "react js": "React",

        "angular": "Angular",
        "vue": "Vue",

        # Backend
        "node": "Node.js",
        "nodejs": "Node.js",
        "node js": "Node.js",
        "node.js": "Node.js",

        "express": "Express",

        "flask": "Flask",

        "django": "Django",

        "fastapi": "FastAPI",

        # Database
        "sql": "SQL",
        "mysql": "MySQL",

        "postgres": "PostgreSQL",
        "postgresql": "PostgreSQL",

        "mongodb": "MongoDB",
        "mongo db": "MongoDB",

        "sqlite": "SQLite",

        "oracle": "Oracle",

        "firebase": "Firebase",

        # AI / ML
        "artificial intelligence": "Artificial Intelligence",
        "artificial intelligence ai": "Artificial Intelligence",
        "ai": "Artificial Intelligence",

        "machine learning": "Machine Learning",
        "machine-learning": "Machine Learning",
        "ml": "Machine Learning",

        "deep learning": "Deep Learning",

        "data science": "Data Science",

        "data analysis": "Data Analysis",
        "data analytics": "Data Analysis",

        "natural language processing": "NLP",
        "nlp": "NLP",

        "computer vision": "Computer Vision",

        "generative ai": "Generative AI",
        "generative artificial intelligence": "Generative AI",
        "gen ai": "Generative AI",

        "large language model": "LLM",
        "large language models": "LLM",
        "llm": "LLM",

        # Python Libraries
        "numpy": "NumPy",

        "pandas": "Pandas",

        "matplotlib": "Matplotlib",

        "opencv": "OpenCV",
        "opencv-python": "OpenCV",
        "opencv python": "OpenCV",

        "scikit learn": "Scikit-Learn",
        "scikit-learn": "Scikit-Learn",
        "sklearn": "Scikit-Learn",

        "tensorflow": "TensorFlow",

        "keras": "Keras",

        "streamlit": "Streamlit",

        # Cloud
        "aws": "AWS",
        "amazon web services": "AWS",

        "azure": "Azure",
        "microsoft azure": "Azure",

        "gcp": "GCP",
        "google cloud": "GCP",

        # Tools
        "git": "Git",
        "github": "GitHub",

        "linux": "Linux",
        "windows": "Windows",

        "vs code": "VS Code",
        "visual studio code": "VS Code",

        "excel": "Microsoft Excel",
        "microsoft excel": "Microsoft Excel",

        "power bi": "Power BI",

        "tableau": "Tableau",

        # Soft Skills
        "communication": "Communication",
        "communication skills": "Communication",

        "leadership": "Leadership",

        "teamwork": "Teamwork",
        "team work": "Teamwork",

        "problem solving": "Problem Solving",
        "problem-solving": "Problem Solving",

        "critical thinking": "Critical Thinking",

        "analytical thinking": "Analytical Thinking",

        "time management": "Time Management",

        "presentation": "Presentation",
        "presentation skills": "Presentation"
    }

    # ----------------------------------
    # Extract Required Skills From JD
    # ----------------------------------

    required_skills = []

    # Check complete aliases
    for alias, standard_skill in jd_skill_aliases.items():

        if alias in jd_text:

            required_skills.append(
                standard_skill
            )

    # ----------------------------------
    # Also Check Main Skills Database
    # ----------------------------------

    for skill in SKILLS_DB:

        skill_lower = skill.lower()

        if skill_lower in [
            "c++",
            "c#",
            "node.js"
        ]:

            pattern = re.escape(
                skill_lower
            )

        else:

            pattern = (
                r"(?<!\w)"
                + re.escape(skill_lower)
                + r"(?!\w)"
            )

        if re.search(
            pattern,
            jd_text
        ):

            normalized_skill = normalize_skill(
                skill
            )

            if normalized_skill:
                required_skills.append(
                    normalized_skill
                )

    # ----------------------------------
    # Clean Required Skills
    # ----------------------------------

    required_skills = clean_skills(
        required_skills
    )

    # ----------------------------------
    # Find Matching Skills
    # ----------------------------------

    matched_skills = []

    missing_skills = []

    for required_skill in required_skills:

        required_key = required_skill.lower()

        if required_key in resume_skill_map:

            matched_skills.append(
                resume_skill_map[required_key]
            )

        else:

            missing_skills.append(
                required_skill
            )

    # ----------------------------------
    # Final Cleanup
    # ----------------------------------

    matched_skills = clean_skills(
        matched_skills
    )

    missing_skills = clean_skills(
        missing_skills
    )

    # ----------------------------------
    # Return Results
    # ----------------------------------

    return (
        resume_skills,
        required_skills,
        missing_skills
    )
# ----------------------------------
# SMART JOB MATCH SCORE
# Version 5.0
# ----------------------------------

def calculate_job_match_score(
    resume_text,
    job_description
):

    # ----------------------------------
    # Empty JD
    # ----------------------------------

    if not job_description or not job_description.strip():

        return 0

    # ----------------------------------
    # Get Skill Gap Analysis
    # ----------------------------------

    (
        resume_skills,
        required_skills,
        missing_skills
    ) = skill_gap_analysis(
        resume_text,
        job_description
    )

    # ----------------------------------
    # No Required Skills
    # ----------------------------------

    if not required_skills:

        return 0

    # ----------------------------------
    # Create Normalized Sets
    # ----------------------------------

    resume_set = {
        normalize_skill(skill).lower()
        for skill in resume_skills
    }

    required_set = {
        normalize_skill(skill).lower()
        for skill in required_skills
    }

    # ----------------------------------
    # Matched Skills
    # ----------------------------------

    matched_skills = (
        resume_set.intersection(
            required_set
        )
    )

    # ----------------------------------
    # Skill Match Percentage
    # ----------------------------------

    skill_match_percentage = (
        len(matched_skills)
        /
        len(required_set)
    ) * 100

    # ----------------------------------
    # Final Score
    # ----------------------------------

    score = int(
        round(skill_match_percentage)
    )

    return min(
        max(score, 0),
        100
    )