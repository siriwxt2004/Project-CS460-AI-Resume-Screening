import spacy

nlp = spacy.load("en_core_web_sm")

def extract_features(text):

    doc = nlp(text)

    skills=[]

    for t in doc:

        if t.is_alpha:

            skills.append(
                t.text
            )

    return {
        "skills":
        list(
            set(
                skills
            )
        )
    }