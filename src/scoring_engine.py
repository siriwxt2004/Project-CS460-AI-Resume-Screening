# scoring_engine.py

import re


# =========================
# VALID SKILLS
# =========================

VALID_SKILLS = [

    # programming
    "python",
    "java",
    "javascript",
    "typescript",
    "php",
    "c",
    "c++",
    "c#",
    "go",
    "dart",
    "kotlin",
    "swift",

    # frontend
    "react",
    "vue",
    "angular",
    "nextjs",
    "tailwind",
    "html",
    "css",
    "bootstrap",

    # backend
    "node.js",
    "node",
    "express",
    "django",
    "flask",
    "fastapi",
    "spring",

    # mobile
    "flutter",
    "android",
    "ios",
    "react native",

    # database
    "sql",
    "mysql",
    "postgresql",
    "mongodb",
    "oracle",
    "pl/sql",

    # devops/cloud
    "docker",
    "kubernetes",
    "aws",
    "azure",
    "gcp",
    "git",
    "ci/cd",
    "jenkins",

    # api/network
    "rest api",
    "api",
    "rest",
    "network",
    "network programming",

    # methodology
    "agile",
    "scrum",

    # support
    "helpdesk",
    "ticketing",
    "call handling",
    "hardware support",
    "it support",
]


# =========================
# CLEAN TEXT
# =========================

def clean_text(text):

    text = text.lower()

    text = re.sub(r"\n", " ", text)
    text = re.sub(r"[.,()\-_/]", " ", text)

    text = re.sub(r"\s+", " ", text)

    return text.strip()


# =========================
# EXTRACT SKILLS
# =========================

def extract_skills(text):

    text = clean_text(text)

    found = []

    for skill in VALID_SKILLS:

        skill_clean = clean_text(skill)

        # exact word match
        pattern = r"\b" + re.escape(skill_clean) + r"\b"

        if re.search(pattern, text):
            found.append(skill)

    return sorted(list(set(found)))


# =========================
# SKILL MATCH
# =========================

def calculate_skill_match(jd_text, resume_text):

    jd_skills = extract_skills(jd_text)

    resume_skills = extract_skills(resume_text)

    matched = []
    missing = []

    for skill in jd_skills:

        if skill in resume_skills:
            matched.append(skill)

        else:
            missing.append(skill)

    # score
    if len(jd_skills) == 0:
        percent = 0
    else:
        percent = int((len(matched) / len(jd_skills)) * 100)

    return {
        "jd_skills": jd_skills,
        "resume_skills": resume_skills,
        "matched": matched,
        "missing": missing,
        "percent": percent,
    }


# =========================
# FINAL SCORE
# =========================

def calculate_final_score(
    semantic_score,
    skill_percent,
    ml_score=0
):

    final_score = (
        (semantic_score * 0.5)
        + (skill_percent * 0.3)
        + (ml_score * 0.2)
    )

    return round(final_score, 2)


# =========================
# VERDICT
# =========================

def get_verdict(score):

    if score >= 75:
        return "ผ่าน"

    elif score >= 50:
        return "พิจารณา"

    else:
        return "ไม่ผ่าน"