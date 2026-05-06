import os
import json
from datetime import datetime

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../")
)

MODELS_DIR = os.path.join(BASE_DIR, "models")

os.makedirs(MODELS_DIR, exist_ok=True)

METRICS_PATH = os.path.join(MODELS_DIR, "metrics.json")
METADATA_PATH = os.path.join(MODELS_DIR, "metadata.json")

def save_metrics(micro_f1, macro_f1, weighted_f1):
    metrics = {
        "micro_f1": round(micro_f1, 4),
        "macro_f1": round(macro_f1, 4),
        "weighted_f1": round(weighted_f1, 4),
        "trained_at": datetime.utcnow().isoformat()
    }

    with open(METRICS_PATH, "w") as f:
        json.dump(metrics, f, indent=4)

def save_metadata():
    metadata = {
        "model_version": "v1",
        "embedding_model": "all-MiniLM-L6-v2",
        "datasets": [
            "CUAD",
            "LEDGAR"
        ],
        "threshold": 0.40,
        "classifier": "SGDClassifier",
        "trained_at": datetime.utcnow().isoformat()
    }

    with open(METADATA_PATH, "w") as f:
        json.dump(metadata, f, indent=4)