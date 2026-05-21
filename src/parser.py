import re

def parse_resume(text):

    profile = {
        "name": "",
        "email": "",
        "phone": "",
        "skills": []
    }

    # email
    email_match = re.search(
        r'[\w\.-]+@[\w\.-]+',
        text
    )

    if email_match:
        profile["email"] = email_match.group(0)

    # phone
    phone_match = re.search(
        r'\d{9,10}',
        text
    )

    if phone_match:
        profile["phone"] = phone_match.group(0)

    # skills
    skills_db = [
        "python",
        "sql",
        "machine learning",
        "nlp",
        "tensorflow",
        "pandas",
        "scikit-learn"
    ]

    found_skills = []

    lower_text = text.lower()

    for skill in skills_db:
        if skill in lower_text:
            found_skills.append(skill)

    profile["skills"] = found_skills

    # name
    lines = text.split("\n")

    if lines:
        profile["name"] = lines[0].strip()

    return profile