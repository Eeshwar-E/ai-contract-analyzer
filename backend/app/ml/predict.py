import os
import joblib
import numpy as np

from app.utils.embedding_utils import get_embedding

BASE_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "../../"
    )
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models/clause_model.pkl"
)

MLB_PATH = os.path.join(
    BASE_DIR,
    "models/mlb.pkl"
)

_model = None
_mlb = None

def load_models():

    global _model
    global _mlb

    if _model is None:

        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(
                f"Missing model file: {MODEL_PATH}"
            )

        _model = joblib.load(MODEL_PATH)

    if _mlb is None:

        if not os.path.exists(MLB_PATH):
            raise FileNotFoundError(
                f"Missing label binarizer: {MLB_PATH}"
            )

        _mlb = joblib.load(MLB_PATH)

    return _model, _mlb

def classify_clause_ml(
    text,
    top_k=3,
    threshold=0.40
):

    model, mlb = load_models()

    emb = get_embedding(text).reshape(1, -1)

    probs = model.predict_proba(emb)[0]

    selected = []

    for idx, prob in enumerate(probs):

        if prob >= threshold:

            selected.append(
                (
                    mlb.classes_[idx],
                    float(prob)
                )
            )

    selected = sorted(
        selected,
        key=lambda x: x[1],
        reverse=True
    )

    if selected:

        best_prob = selected[0][1]

        filtered = []

        for label, prob in selected:

            if prob >= best_prob * 0.55:
                filtered.append(
                    (
                        label,
                        prob
                    )
                )

        selected = filtered

    if not selected:

        top_indices = np.argsort(probs)[::-1]

        best_prob = probs[top_indices[0]]

        selected = []

        for i in top_indices:

            prob = float(probs[i])

            if prob >= best_prob * 0.55:

                selected.append(
                    (
                        mlb.classes_[i],
                        prob
                    )
                )

            if len(selected) >= top_k:
                break

    if selected[0][1] < 0.45:

        return {
            "labels": ["Unknown"],
            "confidence": selected
        }

    selected = selected[:top_k]

    return {
        "labels": [
            label for label, _ in selected
        ],

        "confidence": selected
    }