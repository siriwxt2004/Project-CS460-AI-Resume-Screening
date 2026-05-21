# src/parser.py

import re
import pdfplumber
import docx


SKILLS_DB = [
    "python",
    "java",
    "sql",
    "machine learning",
    "deep learning",
    "nlp",
    "tensorflow",
    "pytorch",
    "scikit-learn",
    "pandas",
    "numpy",
    "data visualization",
    "excel",
    "power bi",
    "tableau",
    "flask",
    "streamlit",
    "git",
]


def extract_text_from_pdf(file):
    text = ""

    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    return text


def extract_text_from_docx(file):
    doc = docx.Document(file)

    text = "\n".join(
        [para.text for para in doc.paragraphs]
    )

    return text


def extract_email(text):
    match = re.search(
        r"[\w\.-]+@[\w\.-]+",
        text
    )

    return match.group(0) if match else "-"


def extract_phone(text):
    match = re.search(
        r"(\+?\d[\d\s\-]{8,15}\d)",
        text
    )

    return match.group(0) if match else "-"


def extract_name(text):
    lines = text.split("\n")

    for line in lines:
        line = line.strip()

        if len(line) > 2 and len(line.split()) <= 4:
            return line

    return "-"


def extract_skills(text):
    text_lower = text.lower()

    found_skills = []

    for skill in SKILLS_DB:
        if skill.lower() in text_lower:
            found_skills.append(skill)

    return list(set(found_skills))


def parse_resume(file):
    text = ""

    # PDF
    if file.name.endswith(".pdf"):
        text = extract_text_from_pdf(file)

    # DOCX
    elif file.name.endswith(".docx"):
        text = extract_text_from_docx(file)

    # TXT
    elif file.name.endswith(".txt"):
        text = file.read().decode("utf-8")

    else:
        return {
            "name": "-",
            "email": "-",
            "phone": "-",
            "skills": [],
            "text": ""
        }

    profile = {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "skills": extract_skills(text),
        "text": text
    }

    return profile