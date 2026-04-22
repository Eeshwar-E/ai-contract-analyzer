def explain_clause(clause: str, risk: str):
    c = clause.lower()

    if "non-refundable" in c:
        return "You may not get your money back under certain conditions."

    if "penalty" in c:
        return "You may need to pay extra charges if conditions are not met."

    if "auto-renew" in c:
        return "This agreement may renew automatically without notice."

    if risk == "High":
        return "This clause may have serious financial or legal consequences."

    elif risk == "Medium":
        return "This clause requires attention before agreeing."

    else:
        return "This clause appears standard."