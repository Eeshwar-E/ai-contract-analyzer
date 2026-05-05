def explain_clause(clause, risk, phrases=None, semantic_matches=None):
    explanation = []

    if phrases:
        for phrase, level in phrases:
            explanation.append(f"Detected phrase: '{phrase}' ({level} risk)")

    if semantic_matches:
        for phrase, level, sim in semantic_matches:
            explanation.append(f"Similar to: '{phrase}' ({level} risk, {sim*100:.2f}%)")

    if not explanation:
        if risk == "High":
            explanation.append("This clause may have serious consequences.")
        elif risk == "Medium":
            explanation.append("This clause needs attention.")
        else:
            explanation.append("This clause appears standard.")

    return " ".join(explanation)