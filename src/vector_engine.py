from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def semantic_search(
    jd_text,
    resumes,
    top_k=5
):

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

            "name": resumes[i]["name"],

            "content": resumes[i]["content"],

            "profile": resumes[i]["profile"],

            "semantic_score": float(score)

        })

    ranked.sort(
        key=lambda x: x["semantic_score"],
        reverse=True
    )

    return ranked[:top_k]