import pandas as pd
import os
import joblib

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, confusion_matrix

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
DATA_PATH = os.path.join(BASE_DIR, "risk_dataset.csv")
MODEL_PATH = os.path.join(BASE_DIR, "models/risk_model.pkl")


def load_data():
    df = pd.read_csv(DATA_PATH)

    df = df[['text', 'label']].dropna()

    # remove very small dataset issues
    df = df[df['text'].str.len() > 20]

    return df


def train():
    df = load_data()

    X = df['text']
    y = df['label']

    if len(df) < 20:
        print("Not enough data to train risk model yet")
        return

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(max_features=5000, ngram_range=(1, 2))),
        ("clf", LogisticRegression(max_iter=1000))
    ])

    pipeline.fit(X_train, y_train)
    y_pred = pipeline.predict(X_test)

    print("\nRisk Model Report:")
    print(classification_report(y_test, y_pred))

    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    acc = pipeline.score(X_test, y_test)
    print(f"Risk Model Accuracy: {acc:.2f}")

    os.makedirs(os.path.join(BASE_DIR, "models"), exist_ok=True)
    joblib.dump(pipeline, MODEL_PATH)

    print("✅ Risk model saved!")


if __name__ == "__main__":
    train()