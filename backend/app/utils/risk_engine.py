from app.utils.ngram_utils import extract_ngrams, detect_phrases
from app.utils.embedding_utils import detect_semantic_risk

def detect_risk(clause: str, label=None, confidence=0.0):
    c = clause.lower()
    score = 0
    
    # 🔹 ML-based boost
    if confidence > 0.7:
        if label in ["Termination for Convenience", "Indemnification"]:
            score += 3
        elif label in ["Payment Terms"]:
            score += 2

    # 🔹 1. Keyword-based scoring (your original logic)
    if "non-refundable" in c:
        score += 3

    if "forfeit" in c:
        score += 3

    if "penalty" in c or "fine" in c:
        score += 2

    if "auto-renew" in c:
        score += 2

    if "must" in c and "pay" in c:
        score += 2

    if "notice" in c:
        score += 1

    # 🔹 2. N-gram phrase detection
    ngrams = extract_ngrams(clause)
    phrases = detect_phrases(ngrams)

    for phrase, level in phrases:
        if level == "high":
            score += 3
        elif level == "medium":
            score += 2

    # 🔹 3. Semantic (embedding-based) detection
    semantic_matches = detect_semantic_risk(clause)

    for phrase, level, sim in semantic_matches:
        if level == "high":
            score += 3 + int(3 * sim)   # weighted by similarity
        elif level == "medium":
            score += 2 + int(2 * sim)

    return score, phrases, semantic_matches


def get_risk_label(score: int):
    if score >= 5:
        return "High"
    elif score >= 2:
        return "Medium"
    else:
        return "Low"