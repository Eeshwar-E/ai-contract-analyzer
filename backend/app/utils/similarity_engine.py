from sklearn.metrics.pairwise import cosine_similarity
from app.utils.embedding_utils import get_embedding

REFERENCE_CLAUSES = [
    {
        "text": "The employee shall maintain confidentiality.",
        "label": "Confidentiality"
    },
    {
        "text": "Either party may terminate this agreement.",
        "label": "Termination"
    },
    {
        "text": "Compensation shall be paid monthly.",
        "label": "Finance"
    }
]

reference_embeddings = [
    get_embedding(item["text"])
    for item in REFERENCE_CLAUSES
]

def get_similar_clauses(clause, top_k=2):

    query_embedding = get_embedding(clause)

    scores = cosine_similarity(
        [query_embedding],
        reference_embeddings
    )[0]

    results = []

    for idx, score in enumerate(scores):

        results.append({
            "label":
                REFERENCE_CLAUSES[idx]["label"],

            "text":
                REFERENCE_CLAUSES[idx]["text"],

            "score":
                round(float(score), 4)
        })

    results = sorted(
        results,
        key=lambda x: x["score"],
        reverse=True
    )

    return results[:top_k]