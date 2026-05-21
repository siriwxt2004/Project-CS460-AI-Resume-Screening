import re


def parse_resume(file):

    text = ""

    # ---------- PDF ----------
    if file.name.endswith(".pdf"):

        import PyPDF2

        pdf = PyPDF2.PdfReader(file)

        for page in pdf.pages:

            t = page.extract_text()

            if t:
                text += t + "\n"

    # ---------- TXT ----------
    elif file.name.endswith(".txt"):

        text = file.read().decode(
            "utf-8",
            errors="ignore"
        )

    # ---------- DOCX ----------
    elif file.name.endswith(".docx"):

        from docx import Document

        doc = Document(file)

        text = "\n".join(
            p.text for p in doc.paragraphs
        )

    # ---------- EMAIL ----------
    email_match = re.search(

        r'[\w\.-]+@[\w\.-]+',

        text

    )

    email = (

        email_match.group(0)

        if email_match

        else "-"

    )

    # ---------- PHONE ----------
    phone_match = re.search(

        r'(\+66|0)[0-9\-]{8,12}',

        text

    )

    phone = (

        phone_match.group(0)

        if phone_match

        else "-"

    )

    # ---------- NAME ----------
    lines = text.split("\n")

    name = "-"

    for line in lines[:5]:

        line = line.strip()

        if len(line) > 3 and len(line) < 40:

            name = line

            break

    # ---------- SKILLS ----------
    skill_keywords = [

        "python",
        "java",
        "javascript",
        "react",
        "flutter",
        "node.js",
        "sql",
        "mysql",
        "docker",
        "aws",
        "machine learning",
        "nlp",
        "tensorflow",
        "pytorch",
        "fastapi",
        "git"

    ]

    found_skills = []

    lower_text = text.lower()

    for skill in skill_keywords:

        if skill.lower() in lower_text:

            found_skills.append(skill)

    return {

        "name": name,

        "email": email,

        "phone": phone,

        "skills": found_skills

    }