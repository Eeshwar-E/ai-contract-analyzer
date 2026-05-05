import pandas as pd
import os
import json

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
DATA_DIR = os.path.join(BASE_DIR, "../data/raw/LEDGAR")
OUTPUT_PATH = os.path.join(BASE_DIR, "../data/processed_ledgar.csv")

# Load label map
with open(os.path.join(DATA_DIR, "label_map.json"), "r") as f:
    LABEL_NAMES = json.load(f)


LABEL_MAP = {
    "confidentiality": "Confidentiality",
    "non-disclosure": "Confidentiality",

    "termination": "Termination",
    "termination for convenience": "Termination",

    "liability": "Liability",
    "limitation of liability": "Liability",

    "governing law": "Governance",
    "jurisdiction": "Governance",

    "assignment": "Transfer",
    "anti-assignment": "Transfer",
}


def normalize_label(label):
    label = label.lower().strip()

    for key in LABEL_MAP:
        if key in label:
            return LABEL_MAP[key]

    return label.title()


def preprocess():
    all_rows = []

    for split in ["train", "validation", "test"]:
        file_path = os.path.join(DATA_DIR, f"{split}.csv")

        df = pd.read_csv(file_path)

        for _, row in df.iterrows():
            text = str(row["text"]).strip()
            label_idx = row["label"]

            # 🔥 Convert index → actual label
            try:
                label_name = LABEL_NAMES[int(label_idx)]
            except:
                continue

            clean_label = normalize_label(label_name)

            if text and clean_label:
                all_rows.append({
                    "text": text,
                    "label": clean_label
                })

    final_df = pd.DataFrame(all_rows)
    final_df = final_df.drop_duplicates()

    final_df.to_csv(OUTPUT_PATH, index=False)

    print("Processed LEDGAR rows:", len(final_df))
    print("Saved to:", OUTPUT_PATH)


if __name__ == "__main__":
    preprocess()