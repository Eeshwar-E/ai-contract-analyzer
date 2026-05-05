import os
import joblib
import numpy as np

from app.utils.embedding_utils import get_embedding

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))

MODEL_PATH = os.path.join(BASE_DIR, "models/clause_model.pkl")
MLB_PATH = os.path.join(BASE_DIR, "models/mlb.pkl")

model = joblib.load(MODEL_PATH)
mlb = joblib.load(MLB_PATH)


def classify_clause_ml(text, top_k=3, threshold=0.4, min_prob=0.2):
    emb = get_embedding(text).reshape(1, -1)

    probs = model.predict_proba(emb)[0]

    # Step 1: Filter low-noise predictions
    candidates = [
        (mlb.classes_[i], float(p))
        for i, p in enumerate(probs)
        if p >= min_prob
    ]

    # Step 2: Apply threshold (main selection)
    selected = [
        (label, prob)
        for label, prob in candidates
        if prob >= threshold
    ]

    # Step 3: Sort by confidence
    selected = sorted(selected, key=lambda x: x[1], reverse=True)

    # Step 4: Fallback to top-K if nothing passes threshold
    if not selected:
        top_indices = np.argsort(probs)[::-1][:top_k]
        selected = [(mlb.classes_[i], float(probs[i])) for i in top_indices]

    # Step 5: Unknown detection (clean + stable)
    if selected[0][1] < threshold:
        return {
            "labels": ["Unknown"],
            "confidence": selected[:top_k]
        }

    # Step 6: Limit to top-K
    selected = selected[:top_k]

    return {
        "labels": [label for label, _ in selected],
        "confidence": selected
    }