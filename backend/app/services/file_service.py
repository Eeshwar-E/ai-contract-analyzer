import os
from app.core.config import UPLOAD_DIR
from app.utils.pdf_utils import extract_text
from app.utils.clause_utils import split_clauses
from app.utils.classifier import classify_clause, apply_length_penalty
from app.utils.risk_engine import detect_risk
from app.utils.explainer import explain_clause

def save_file(content: bytes, filename: str) -> str:
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as f:
        f.write(content)

    return file_path

def process_file(file_path: str):
    text = extract_text(file_path)
    clauses = split_clauses(text)

    results = []

    for clause in clauses:
        category, confidence = classify_clause(clause)
        confidence = apply_length_penalty(confidence, clause)
        risk = detect_risk(clause)
        explanation = explain_clause(clause, risk)

        results.append({
            "text": clause,
            "type": category,
            "confidence": confidence,
            "risk": risk,
            "explanation": explanation
        })

    return results