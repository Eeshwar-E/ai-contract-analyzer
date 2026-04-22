from app.utils.ngram_utils import extract_ngrams, detect_phrases

def detect_risk(clause: str):
    c = clause.lower()

    score = 0

    # High-risk signals
    if "non-refundable" in c:
        score += 3

    if "forfeit" in c:
        score += 3

    # Medium-risk signals
    if "penalty" in c or "fine" in c:
        score += 2

    if "auto-renew" in c:
        score += 2

    if "must" in c and "pay" in c:
        score += 2

    # Low-risk signals
    if "notice" in c:
        score += 1

    ngrams = extract_ngrams(clause)
    phrases = detect_phrases(ngrams)

    for phrase, level in phrases:
        if level == "high":
            score += 3
        elif level == "medium":
            score += 2
    
    return score, phrases

def get_risk_label(score: int):
    if score >= 6:
        return "High"
    elif score >= 3:
        return "Medium"
    else:
        return "Low"