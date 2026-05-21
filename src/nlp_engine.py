import re

def extract_features(text):
    text = text.lower()

    skills = [
        "python",
        "java",
        "sql",
        "machine learning",
        "data analysis",
        "communication",
        "leadership",
        "tensorflow",
        "pandas"
    ]

    found_skills = []

    for skill in skills:
        if skill in text:
            found_skills.append(skill)

    return {
        "skills": found_skills,
        "word_count": len(text.split())
    }