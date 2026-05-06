import json
import pandas as pd
import os
import re

from app.ml.taxonomy import TAXONOMY_MAP

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
DATA_PATH = os.path.join(BASE_DIR,"../data/raw/CUAD_v1/CUAD_v1.json")
OUTPUT_PATH = os.path.join(BASE_DIR,"../data/processed_clauses.csv")

def extract_label(question):
    match = re.search(r'"(.*?)"', question)
    if match:
        return match.group(1).strip()
    if "related to" in question:
        try:
            return (
                question
                .split("related to")[1]
                .split("that")[0]
                .strip()
            )
        except:
            pass

    return question.strip()

def normalize_label(label):
    label = label.strip()
    return TAXONOMY_MAP.get(label, None)

def preprocess():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    rows = []
    for doc in data["data"]:
        for para in doc["paragraphs"]:
            for qa in para["qas"]:
                raw_label = extract_label(qa["question"])
                clean_label = normalize_label(raw_label)
                if clean_label is None:
                    continue
                for ans in qa.get("answers", []):
                    clause_text = ans.get("text", "").strip()
                    if clause_text and clean_label is not None:
                        rows.append({
                            "text": clause_text,
                            "label": clean_label
                        })

    df = pd.DataFrame(rows)
    df = df.drop_duplicates()
    df = df.dropna()
    df = df[
        df["text"].str.split().str.len() > 5
    ]
    df.to_csv(OUTPUT_PATH, index=False)

    print("Processed CUAD rows:", len(df))
    print("Unique labels:", df["label"].nunique())
    print("Saved to:", OUTPUT_PATH)

if __name__ == "__main__":
    preprocess()