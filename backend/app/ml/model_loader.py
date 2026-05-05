import os
import joblib

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
MODEL_PATH = os.path.join(BASE_DIR, "models/clause_model.pkl")

model = None


def load_model():
    global model
    if model is None:
        model = joblib.load(MODEL_PATH)
    return model