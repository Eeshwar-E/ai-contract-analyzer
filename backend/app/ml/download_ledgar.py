from datasets import load_dataset
import pandas as pd
import os
import json

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
OUTPUT_DIR = os.path.join(BASE_DIR, "../data/raw/LEDGAR")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load dataset
dataset = load_dataset("lex_glue", "ledgar")

# 🔥 Extract label names
label_names = dataset["train"].features["label"].names

# Save label mapping
with open(os.path.join(OUTPUT_DIR, "label_map.json"), "w") as f:
    json.dump(label_names, f)

# Save splits
for split in ["train", "validation", "test"]:
    df = pd.DataFrame(dataset[split])
    df.to_csv(os.path.join(OUTPUT_DIR, f"{split}.csv"), index=False)

print("LEDGAR dataset downloaded with label mapping.")