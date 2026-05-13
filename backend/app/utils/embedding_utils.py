import requests
import numpy as np
import os

HF_TOKEN = os.getenv("HF_TOKEN")

API_URL = (
    "https://api-inference.huggingface.co/"
    "pipeline/feature-extraction/"
    "sentence-transformers/all-MiniLM-L6-v2"
)

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