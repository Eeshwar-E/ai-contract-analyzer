import requests
import numpy as np
import os
from sklearn.metrics.pairwise import cosine_similarity

HF_TOKEN = os.getenv("HF_TOKEN")

API_URL = (
    "https://api-inference.huggingface.co/"
    "pipeline/feature-extraction/"
    "sentence-transformers/all-MiniLM-L6-v2"
)

REFERENCE_PHRASES = {
    "high": [
        "terminate for convenience",
        "without prior notice",
        "sole discretion",
        "indemnify and hold harmless",
        "not liable for any damages"
    ],
    "medium": [
        "late payment fee",
        "automatic renewal",
        "subject to change"
    ]
}

headers = {
    "Authorization": f"Bearer {HF_TOKEN}"
}

def get_embedding(text: str):

    response = requests.post(
        API_URL,
        headers=headers,
        json={
            "inputs": text
        },
        timeout=60
    )

    if response.status_code != 200:
        raise Exception(
            f"HF API Error: {response.text}"
        )

    embedding = response.json()

    return np.array(embedding).mean(axis=0)

def get_embedding_batch(texts):

    embeddings = []

    for text in texts:
        embeddings.append(
            get_embedding(text)
        )

    return embeddings


def detect_semantic_risk(clause: str):
    clause_embedding = get_embedding(clause)
    detected = []

    for level, phrases in REFERENCE_PHRASES.items():
        for phrase in phrases:
            phrase_embedding = get_embedding(phrase)

            score = cosine_similarity(
                [clause_embedding],
                [phrase_embedding]
            )[0][0]

            if score > 0.45:
                detected.append(
                    (
                        phrase,
                        level,
                        float(score)
                    )
                )

    return detected