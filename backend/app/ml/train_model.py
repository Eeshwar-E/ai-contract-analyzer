import pandas as pd
import os
import joblib
from itertools import chain
from collections import Counter

from sklearn.model_selection import train_test_split

from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.multiclass import OneVsRestClassifier
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.metrics import classification_report, f1_score

from app.utils.embedding_utils import get_embedding_batch
from app.utils.model_utils import save_metrics, save_metadata

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
DATA_PATH = os.path.join(BASE_DIR, "../data/final_merged_dataset.csv")
MODEL_PATH = os.path.join(BASE_DIR, "models/clause_model.pkl")
MLB_PATH = os.path.join(BASE_DIR, "models/mlb.pkl")


def load_data():
    df = pd.read_csv(DATA_PATH)

    df = df[['text', 'label']].dropna()

    grouped = (
    df.groupby("text")["label"]
    .apply(lambda labels: list(set(
                chain.from_iterable(
                    l if isinstance(l, list) else [l] for l in labels
                )
            )
        )
    ).reset_index())

    return grouped

def train():
    df = load_data()

    # Remove low-support labels
    all_labels = list(chain.from_iterable(df["label"]))

    label_counts = Counter(all_labels)

    valid_labels = {
        label for label, count in label_counts.items()
        if count >= 25
    }
    df["label"] = df["label"].apply(
        lambda labels: [l for l in labels if l in valid_labels]
    )

    print("Remaining labels:", len(valid_labels))
    print("Remaining rows:", len(df))

    df = df[df["label"].map(len) > 0]

    X = df["text"]
    y = df["label"]

    # Convert labels -> binary vectors
    mlb = MultiLabelBinarizer()
    y_bin = mlb.fit_transform(y)

    # Generate embeddings
    X_embed = get_embedding_batch(X.tolist())

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X_embed,
        y_bin,
        test_size=0.2,
        random_state=42
    )

    # Train model
    model = OneVsRestClassifier(
        SGDClassifier(loss="log_loss")
    )

    model.fit(X_train, y_train)

    # Predict probabilities
    probs = model.predict_proba(X_test)

    # Threshold-based prediction
    threshold = 0.40
    y_pred = (probs >= threshold).astype(int)

    # Evaluation
    report = classification_report(
        y_test,
        y_pred,
        target_names=mlb.classes_,
        zero_division=0
    )

    print(report)

    micro_f1 = f1_score(
        y_test,
        y_pred,
        average="micro"
    )

    macro_f1 = f1_score(
        y_test,
        y_pred,
        average="macro"
    )

    weighted_f1 = f1_score(
        y_test,
        y_pred,
        average="weighted"
    )

    save_metrics(
        micro_f1,
        macro_f1,
        weighted_f1
    )

    save_metadata()

    # Save model artifacts
    os.makedirs(os.path.join(BASE_DIR, "models"), exist_ok=True)

    joblib.dump(model, MODEL_PATH)
    joblib.dump(mlb, MLB_PATH)

    print("Multi-label model saved")


if __name__ == "__main__":
    train()