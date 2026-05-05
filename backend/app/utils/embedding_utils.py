from sentence_transformers import SentenceTransformer, util
import numpy as np

# 🔹 Load model once
_model = SentenceTransformer("all-MiniLM-L6-v2")


# =========================
# 🔹 CORE EMBEDDING METHODS
# =========================

def get_embedding(text: str):
    """
    Convert single text → embedding vector
    """
    return _model.encode(text)


def get_embedding_batch(texts):
    """
    Convert list of texts → embeddings (faster for training)
    """
    return _model.encode(texts, batch_size=32, show_progress_bar=True)


# =========================
# 🔹 SEMANTIC RISK DETECTION
# =========================

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

# Precompute embeddings once
reference_embeddings = {
    level: _model.encode(phrases, convert_to_tensor=True)
    for level, phrases in REFERENCE_PHRASES.items()
}


def detect_semantic_risk(clause: str):
    """
    Detect semantic similarity to risky phrases
    """
    clause_embedding = _model.encode(clause, convert_to_tensor=True)

    detected = []

    for level, embeddings in reference_embeddings.items():
        scores = util.cos_sim(clause_embedding, embeddings)[0]

        for i, score in enumerate(scores):
            if score > 0.45:  # threshold (tune later)
                phrase = REFERENCE_PHRASES[level][i]
                detected.append((phrase, level, float(score)))

    return detected