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

    # Final decision
    if score >= 4:
        return "High"
    elif score >= 2:
        return "Medium"
    else:
        return "Low"