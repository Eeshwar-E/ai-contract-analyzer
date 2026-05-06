import pandas as pd
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))

CUAD_PATH = os.path.join(BASE_DIR, "../data/processed_clauses.csv")
LEDGAR_PATH = os.path.join(BASE_DIR, "../data/processed_ledgar.csv")

OUTPUT_PATH = os.path.join(BASE_DIR, "../data/final_merged_dataset.csv")


def merge():
    cuad_df = pd.read_csv(CUAD_PATH)
    ledgar_df = pd.read_csv(LEDGAR_PATH)

    # Keep only required columns
    cuad_df = cuad_df[["text", "label"]]
    ledgar_df = ledgar_df[["text", "label"]]

    # Merge datasets
    merged_df = pd.concat([cuad_df, ledgar_df], ignore_index=True)

    # Remove duplicates
    merged_df = merged_df.drop_duplicates()

    # Remove empty rows
    merged_df = merged_df.dropna()

    # Remove very short clauses
    merged_df = merged_df[
        merged_df["text"].str.split().str.len() > 5
    ]

    merged_df.to_csv(OUTPUT_PATH, index=False)

    print("CUAD rows:", len(cuad_df))
    print("LEDGAR rows:", len(ledgar_df))
    print("Merged rows:", len(merged_df))
    print("Saved to:", OUTPUT_PATH)


if __name__ == "__main__":
    merge()