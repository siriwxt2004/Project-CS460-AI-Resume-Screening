import re
import spacy

nlp = spacy.load(
    "en_core_web_sm"
)

EMAIL = r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}'


def parse_resume(text):

    doc = nlp(text)

    name = ""

    for ent in doc.ents:

        if ent.label_ == "PERSON":

            name = ent.text

            break

    email = ""

    found = re.findall(
        EMAIL,
        text
    )

    if found:

        email = found[0]

    skills = []

    known = [

        "python",
        "java",
        "javascript",
        "react",
        "nodejs",
        "sql",
        "docker",
        "aws",
        "git",
        "linux",
        "windows",
        "network",
        "helpdesk",
        "ticketing"

    ]

    lower = text.lower()

    for s in known:

        if s in lower:

            skills.append(
                s
            )

    return {

        "name": name,

        "email": email,

        "skills": skills

    }