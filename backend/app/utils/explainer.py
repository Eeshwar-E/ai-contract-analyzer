def explain_clause(clause: str, risk: str, phrases=None):
    c = clause.lower()
    explanation = []

    # Phrase-based explanations (NEW)
    if phrases:
        for phrase, level in phrases:
            explanation.append(f"Detected phrase: '{phrase}' ({level} risk)")

    # Existing keyword explanations
    if "non-refundable" in c:
        explanation.append("You may not get your money back under certain conditions.")

    if "penalty" in c:
        explanation.append("You may need to pay extra charges if conditions are not met.")

    if "auto-renew" in c:
        explanation.append("This agreement may renew automatically without notice.")

    # Fallback based on risk
    if not explanation:
        if risk == "High":
            explanation.append("This clause may have serious financial or legal consequences.")
        elif risk == "Medium":
            explanation.append("This clause requires attention before agreeing.")
        else:
            explanation.append("This clause appears standard.")

    return " ".join(explanation)