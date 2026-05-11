import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.linear_model import SGDClassifier
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import (
    classification_report,
    confusion_matrix
)

from app.utils.embedding_utils import get_embedding_batch

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../")
)

DATA_PATH = os.path.join(
    BASE_DIR,
    "risk_dataset.csv"
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models/risk_model.pkl"
)

def load_data():
    df = pd.read_csv(DATA_PATH)

    df = df[["text", "label"]].dropna()

    df["text"] = df["text"].astype(str)

    df = df[
        df["text"].str.split().str.len() >= 8
    ]

    return df

def train():
    df = load_data()

    print("Risk samples:", len(df))

    if len(df) < 50:
        print("Not enough data to train risk model")
        return

    X = df["text"]
    y = df["label"]

    # Generate semantic embeddings
    X_embed = get_embedding_batch(
        X.tolist()
    )

    X_train, X_test, y_train, y_test = train_test_split(
        X_embed,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    base_model = SGDClassifier(
        loss="log_loss",
        class_weight="balanced",
        max_iter=3000,
        tol=1e-3
    )

    model = CalibratedClassifierCV(
        base_model,
        cv=3
    )

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    print("\nRisk Model Report:\n")

    print(
        classification_report(
            y_test,
            y_pred,
            zero_division=0
        )
    )

    print("\nConfusion Matrix:\n")

    print(
        confusion_matrix(
            y_test,
            y_pred
        )
    )

    acc = model.score(X_test, y_test)

    print(f"\nRisk Model Accuracy: {acc:.2f}")

    os.makedirs(
        os.path.join(BASE_DIR, "models"),
        exist_ok=True
    )

    joblib.dump(model, MODEL_PATH)

    print("\nRisk model saved")

if __name__ == "__main__":
    train()