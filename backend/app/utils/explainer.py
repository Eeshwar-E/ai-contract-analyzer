def explain_clause(
    clause,
    predictions,
    risk,
    phrases,
    semantic_matches
):
    explanations = []

    if predictions:
        top = predictions[0]

        explanations.append(
            f"This clause is primarily related to "
            f"{top['label']} "
            f"({round(top['confidence'] * 100)}% confidence)."
        )

    if semantic_matches:
        best = semantic_matches[0]

        explanations.append(
            f"It is semantically similar to "
            f"'{best[0]}' "
            f"({round(best[2] * 100)}% similarity)."
        )

    if phrases:
        explanations.append(
            "Risk-related phrases were detected."
        )

    if risk["level"] == "High":
        explanations.append(
            "This clause may introduce significant legal obligations or liability."
        )

    elif risk["level"] == "Medium":
        explanations.append(
            "This clause contains potentially important contractual conditions."
        )

    else:
        explanations.append(
            "This clause appears relatively standard."
        )

    return " ".join(explanations)