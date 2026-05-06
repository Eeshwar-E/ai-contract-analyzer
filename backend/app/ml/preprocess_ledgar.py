import pandas as pd
import os
import json

from app.ml.taxonomy import TAXONOMY_MAP

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
DATA_DIR = os.path.join(BASE_DIR,"../data/raw/LEDGAR")
OUTPUT_PATH = os.path.join(BASE_DIR,"../data/processed_ledgar.csv")

with open(os.path.join(DATA_DIR, "label_map.json"), "r") as f:
    LABEL_NAMES = json.load(f)

def normalize_label(label):
    label = label.strip()
    return TAXONOMY_MAP.get(label, None)

def preprocess():
    all_rows = []
    for split in ["train", "validation", "test"]:
        file_path = os.path.join(DATA_DIR, f"{split}.csv")
        df = pd.read_csv(file_path)
        for _, row in df.iterrows():
            text = str(row["text"]).strip()
            label_idx = row["label"]
            try:
                raw_label = LABEL_NAMES[int(label_idx)]
            except:
                continue
            clean_label = normalize_label(raw_label)
            if clean_label is None:
                continue
            if text and clean_label is not None:
                all_rows.append({
                    "text": text,
                    "label": clean_label
                })
    final_df = pd.DataFrame(all_rows)
    final_df = final_df.drop_duplicates()
    final_df = final_df.dropna()
    final_df = final_df[
        final_df["text"].str.split().str.len() > 5
    ]
    final_df.to_csv(OUTPUT_PATH, index=False)

    print("Processed LEDGAR rows:", len(final_df))
    print("Unique labels:", final_df["label"].nunique())
    print("Saved to:", OUTPUT_PATH)

if __name__ == "__main__":
    preprocess()