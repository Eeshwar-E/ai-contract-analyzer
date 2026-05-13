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
from app.utils.document_classifier import classify_document
from app.utils.similarity_engine import get_similar_clauses

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
        "agreement",
        "party",
        "liability",
        "termination",
        "obligation",
        "indemnify",
        "employment",
        "confidential",
        "payment",
        "law",
        "contract"
    ]

    clause_lower = clause.lower()

    return any(k in clause_lower for k in keywords)

def process_file(file_path: str):
    text = extract_text(file_path)

    if not text or not isinstance(text, str):
        raise ValueError(
            "Failed to extract readable text from PDF"
        )

    clauses = split_clauses(text)

    results = []

    for clause in clauses:

        if not is_legal_clause(clause):
            continue

        # Clause classification
        result = classify_clause(clause)

        top_labels = result["labels"]
        top_scores = result["confidence"]

        category = top_labels[0]
        confidence = top_scores[0][1]

        confidence = apply_length_penalty(
            confidence,
            clause
        )

        if confidence < 0.5:
            category = "Unknown"

        predictions = [
            {
                "label": label,
                "confidence": round(conf, 4)
            }
            for label, conf in top_scores
        ]

        # Risk analysis
        score, phrases, semantic_matches = detect_risk(
            clause,
            label=category,
            confidence=confidence
        )

        try:
            risk_result = predict_risk_ml(clause)

            risk = risk_result["risk"]
            risk_conf = risk_result["confidence"]

            if risk_conf < 0.6:
                risk = get_risk_label(score)

            logger.info(
                f"Clause classified | Labels: {top_labels} | Risk: {risk}"
            )

        except Exception as e:
            logger.error(str(e))

            risk = get_risk_label(score)
            risk_conf = 0.0

        save_training_data(clause, risk)

        explanation = explain_clause(
            clause,
            predictions,
            {
                "level": risk,
                "confidence": risk_conf
            },
            phrases,
            semantic_matches
        )
        similar_clauses = get_similar_clauses(clause)
        results.append({
            "clause": clause,
            "predictions": predictions,
            "risk": {
                "level": risk,
                "confidence": round(risk_conf, 4)
            },
            "rule_based_score": score,
            "semantic_matches": [
                {
                    "phrase": str(m[0]),
                    "risk": str(m[1]),
                    "score": float(m[2])
                }
                for m in semantic_matches
            ],

            "phrases": [str(p) for p in phrases],
            "explanation": explanation,
            "similar_clauses": similar_clauses
        })
    document_summary = classify_document(results)

    return {
        "document_summary": document_summary,
        "clauses": results
    }