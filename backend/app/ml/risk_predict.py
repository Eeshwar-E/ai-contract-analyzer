import os
import joblib

from app.utils.embedding_utils import get_embedding

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../")
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models/risk_model.pkl"
)

model = joblib.load(MODEL_PATH)

def predict_risk_ml(text):
    emb = get_embedding(text).reshape(1, -1)

    probs = model.predict_proba(emb)[0]

    classes = model.classes_

    best_idx = probs.argmax()

    risk = classes[best_idx]

    confidence = min(
        float(probs[best_idx]),
        0.95
    )
    return {
        "risk": risk,
        "confidence": confidence,
        "all_scores": {
            cls: float(prob)
            for cls, prob in zip(classes, probs)
        }
    }