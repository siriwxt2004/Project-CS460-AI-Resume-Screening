import numpy as np
import faiss

from sentence_transformers import SentenceTransformer

# =========================
# LOAD MODEL
# =========================

model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

# =========================
# EMBEDDING
# =========================

def get_embedding(text):

    embedding = model.encode(
        [text]
    )

    return np.array(
        embedding
    ).astype("float32")

# =========================
# SEMANTIC SEARCH
# =========================

def semantic_search(

    jd_text,

    resumes,

    top_k=10

):

    # ---------- JD VECTOR ----------

    jd_vector = get_embedding(
        jd_text
    )

    # ---------- RESUME VECTOR ----------

    vectors = []

    for r in resumes:

        vec = model.encode(
            [r["content"]]
        )[0]

        vectors.append(
            vec
        )

    vectors = np.array(
        vectors
    ).astype("float32")

    # ---------- FAISS ----------

    dimension = vectors.shape[1]

    index = faiss.IndexFlatL2(
        dimension
    )

    index.add(
        vectors
    )

    # ---------- SEARCH ----------

    distances, indices = index.search(

        jd_vector,

        min(
            top_k,
            len(resumes)
        )

    )

    # ---------- RESULT ----------

    results = []

    for idx in indices[0]:

        results.append(
            resumes[idx]
        )

    return results