CATEGORY_KEYWORDS = {
    "Payment": {
        "payment": 3,
        "fee": 2,
        "rent": 3,
        "amount": 2,
        "charges": 2,
        "compensation": 1
    },
    "Penalty": {
        "penalty": 3,
        "fine": 3,
        "breach": 2,
        "violation": 2,
        "damages": 2
    },
    "Deposit": {
        "deposit": 3,
        "security deposit": 3,
        "advance": 2,
        "refundable": 1,
        "non-refundable": 3
    },
    "Termination": {
        "terminate": 3,
        "termination": 3,
        "cancel": 2,
        "expiry": 1
    },
    "Notice": {
        "notice": 2,
        "written notice": 3,
        "inform": 1,
        "notification": 1
    }
}

def classify_clause(clause: str):
    text = clause.lower()
    scores = {}

    for category, keywords in CATEGORY_KEYWORDS.items():
        score = 0
        for kw, weight in keywords.items():
            if kw in text:
                score += weight
        scores[category] = score

    best_category = max(scores, key=scores.get)
    best_score = scores[best_category]
    total_score = sum(scores.values())

    if best_score == 0:
        return "Other", 0.0

    confidence = best_score / (total_score + 1)

    return best_category, round(confidence, 2)

def apply_length_penalty(confidence, clause):
    word_count = len(clause.split())

    if word_count > 40:
        confidence *= 0.8
    elif word_count > 25:
        confidence *= 0.9

    return round(confidence, 2)