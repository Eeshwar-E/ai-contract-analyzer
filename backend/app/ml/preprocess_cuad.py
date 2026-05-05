import json
import pandas as pd
import os
import re

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
DATA_PATH = os.path.join(BASE_DIR, "../data/raw/CUAD_v1/CUAD_v1.json")
OUTPUT_PATH = os.path.join(BASE_DIR, "../data/processed_clauses.csv")


def extract_label(question):
    """
    Extract clean label from CUAD question string
    Example:
    'Highlight the parts ... related to "Audit Rights"...'
    → 'Audit Rights'
    """

    # Try extracting inside quotes
    match = re.search(r'"(.*?)"', question)
    if match:
        return match.group(1).strip()

    # Fallback: extract after 'related to'
    if "related to" in question:
        try:
            return question.split("related to")[1].split("that")[0].strip()
        except:
            pass

    # Final fallback
    return question.strip()


def preprocess():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    rows = []

    for doc in data["data"]:
        for para in doc["paragraphs"]:
            for qa in para["qas"]:
                label = extract_label(qa["question"])

                for ans in qa.get("answers", []):
                    clause_text = ans.get("text", "").strip()

                    if clause_text:
                        rows.append({
                            "text": clause_text,
                            "label": label
                        })

    df = pd.DataFrame(rows)
    df = df.drop_duplicates()

    df.to_csv(OUTPUT_PATH, index=False)

    print("Extracted clauses:", len(df))
    print("Saved to:", OUTPUT_PATH)


if __name__ == "__main__":
    preprocess()