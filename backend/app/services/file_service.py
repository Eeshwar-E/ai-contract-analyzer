import os
import csv
from app.core.config import UPLOAD_DIR
from app.utils.pdf_utils import extract_text
from app.utils.clause_utils import split_clauses
from app.utils.classifier import classify_clause, apply_length_penalty
from app.utils.risk_engine import detect_risk, get_risk_label
from app.utils.explainer import explain_clause
from app.ml.risk_predict import predict_risk_ml
from app.utils.logger import logger

DATASET_PATH = "risk_dataset.csv"

def save_training_data(clause, risk):
    file_exists = os.path.isfile(DATASET_PATH)

    with open(DATASET_PATH, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow(["text", "label"])

        writer.writerow([clause, risk])

def save_file(content: bytes, filename: str) -> str:
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    file_path = os.path.join(UPLOAD_DIR, filename)
    logger.info(f"Uploaded file: {filename}")
    with open(file_path, "wb") as f:
        f.write(content)

    return file_path

def is_legal_clause(clause):
    keywords = [
        "agreement", "party", "liability",
        "termination", "obligation", "indemnify"
    ]
    return any(k in clause.lower() for k in keywords)


def process_file(file_path: str):
    text = extract_text(file_path)
    clauses = split_clauses(text)
    results = []

    for clause in clauses:

        # 🔹 Skip non-legal / junk clauses
        if not is_legal_clause(clause):
            continue

        # 🔹 Clause classification (Model 1 - UPDATED)
        result = classify_clause(clause)

        top_labels = result["labels"]
        top_scores = result["confidence"]

        category = top_labels[0]
        confidence = top_scores[0][1]

        confidence = apply_length_penalty(confidence, clause)

        # 🔹 Unknown handling
        if confidence < 0.5:
            category = "Unknown"

        # 🔹 Always compute rule-based signals (for explanation)
        score, phrases, semantic_matches = detect_risk(
            clause,
            label=category,
            confidence=confidence
        )

        # 🔹 Risk prediction (Model 2)
        try:
            risk_result = predict_risk_ml(clause)
            risk = risk_result["risk"]
            risk_conf = risk_result["confidence"]
            logger.info(
                f"Clause classified | Labels: {result['labels']} | Risk: {risk}"
            )
            # fallback if low confidence
            if risk_conf < 0.6:
                risk = get_risk_label(score)

        except Exception:
            risk = get_risk_label(score)
            risk_conf = 0.0
            logger.error(str(Exception))

        # 🔹 Save training data
        save_training_data(clause, risk)

        # 🔹 Explanation
        explanation = explain_clause(clause, risk, phrases, semantic_matches)

        results.append({
            "clause": clause,
            "predictions": [
                {
                    "label": label,
                    "confidence": round(conf, 4)
                }
                for label, conf in result["confidence"]
            ],
            "risk": {
                "level": risk,
                "confidence": round(risk_conf, 4)
            },
            "rule_based_score": score,
            "semantic_matches": semantic_matches,
            "phrases": phrases,
            "explanation": explanation
        })

    return results