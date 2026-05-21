from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def semantic_search(jd_text, resumes):

    documents = [jd_text]

    for r in resumes:
        documents.append(r["content"])

    vectorizer = TfidfVectorizer(
        stop_words="english"
    )

    vectors = vectorizer.fit_transform(
        documents
    )

    jd_vector = vectors[0:1]

    resume_vectors = vectors[1:]

    similarities = cosine_similarity(
        jd_vector,
        resume_vectors
    )[0]

    ranked = []

    for i, score in enumerate(similarities):

        ranked.append({

            "resume": resumes[i],
            "score": float(score)

        })

    ranked.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return ranked