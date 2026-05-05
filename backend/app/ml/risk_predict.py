from app.ml.risk_loader import load_risk_model


def predict_risk_ml(text):
    model = load_risk_model()

    pred = model.predict([text])[0]
    probs = model.predict_proba([text])[0]

    confidence = max(probs)

    return {
        "risk": pred,
        "confidence": float(confidence)
    }