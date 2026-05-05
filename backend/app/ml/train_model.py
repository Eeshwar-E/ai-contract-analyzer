import pandas as pd
import os
import joblib

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.multiclass import OneVsRestClassifier
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.metrics import classification_report

from app.utils.embedding_utils import get_embedding_batch

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
DATA_PATH = os.path.join(BASE_DIR, "../data/processed_clauses.csv")
MODEL_PATH = os.path.join(BASE_DIR, "models/clause_model.pkl")
MLB_PATH = os.path.join(BASE_DIR, "models/mlb.pkl")


def load_data():
    df = pd.read_csv(DATA_PATH)

    df = df[['text', 'label']].dropna()

    # group labels → multi-label
    grouped = df.groupby("text")["label"].apply(list).reset_index()

    return grouped


def train():
    df = load_data()

    X = df["text"]
    y = df["label"]

    # Convert labels → binary vectors
    mlb = MultiLabelBinarizer()
    y_bin = mlb.fit_transform(y)

    # 🔥 UPDATED: batch embeddings
    X_embed = get_embedding_batch(X.tolist())

    X_train, X_test, y_train, y_test = train_test_split(
        X_embed, y_bin, test_size=0.2, random_state=42
    )

    model = OneVsRestClassifier(SGDClassifier(loss="log_loss", class_weight="balanced"))
    model.fit(X_train, y_train)

    probs = model.predict_proba(X_test)

    threshold = 0.40
    y_pred = (probs >= threshold).astype(int)

    print(classification_report(
        y_test,
        y_pred,
        target_names=mlb.classes_,
        zero_division=0
    ))

    os.makedirs(os.path.join(BASE_DIR, "models"), exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    joblib.dump(mlb, MLB_PATH)

    print("✅ Multi-label model saved")


if __name__ == "__main__":
    train()