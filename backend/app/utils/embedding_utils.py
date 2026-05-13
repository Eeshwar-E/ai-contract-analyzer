from sentence_transformers import SentenceTransformer, util
import numpy as np

_model = None
_reference_embeddings = None

REFERENCE_PHRASES = {
    "high": [
        "terminate for convenience",
        "not liable for damages",
        "indemnify the company",
        "we can cancel anytime"
    ],

    "medium": [
        "late payment fee",
        "auto renewal",
        "subject to change"
    ]
}

def get_model():
    global _model

    if _model is None:
        _model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )

    return _model

def get_reference_embeddings():
    global _reference_embeddings

    if _reference_embeddings is None:

        model = get_model()

        _reference_embeddings = {
            level: model.encode(
                phrases,
                convert_to_tensor=True
            )
            for level, phrases
            in REFERENCE_PHRASES.items()
        }

    return _reference_embeddings

def get_embedding(text: str):
    model = get_model()

    return model.encode(text)

def get_embedding_batch(texts):
    model = get_model()

    return model.encode(
        texts,
        batch_size=16,
        show_progress_bar=True
    )

def detect_semantic_risk(clause: str):

    model = get_model()

    reference_embeddings = (
        get_reference_embeddings()
    )

    clause_embedding = model.encode(
        clause,
        convert_to_tensor=True
    )

    detected = []

    for level, embeddings in reference_embeddings.items():

        scores = util.cos_sim(
            clause_embedding,
            embeddings
        )[0]

        for i, score in enumerate(scores):

            if score > 0.45:

                phrase = (
                    REFERENCE_PHRASES[level][i]
                )

                detected.append(
                    (
                        phrase,
                        level,
                        float(score)
                    )
                )

    return detected