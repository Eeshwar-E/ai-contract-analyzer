from collections import Counter

DOCUMENT_RULES = {
    "Employment Agreement": [
        "Employment",
        "Finance",
        "Confidentiality"
    ],

    "Non-Disclosure Agreement": [
        "Confidentiality",
        "IP"
    ],

    "Vendor Agreement": [
        "Finance",
        "Liability",
        "Governance"
    ],

    "Service Agreement": [
        "Liability",
        "Governance",
        "Termination"
    ],

    "IP Agreement": [
        "IP",
        "Confidentiality"
    ]
}

def classify_document(results):
    labels = []

    if not results:
        return {
            "document_type": "Unknown",
            "confidence": 0.0,
            "detected_labels": {}
        }

    for clause in results:

        predictions = clause.get(
            "predictions",
            []
        )

        if not predictions:
            continue

        for pred in predictions:

            if not isinstance(pred, dict):
                continue

            label = pred.get(
                "label",
                "Unknown"
            )

            confidence = pred.get(
                "confidence",
                0
            )

            if confidence >= 0.50:
                labels.append(label)

    if not labels:
        return {
            "document_type": "Unknown",
            "confidence": 0.0,
            "detected_labels": {}
        }

    label_counts = Counter(labels)

    best_doc = "Unknown"
    best_score = 0

    for doc_type, required_labels in DOCUMENT_RULES.items():

        score = 0

        for label in required_labels:
            score += label_counts.get(
                label,
                0
            )

        if score > best_score:
            best_score = score
            best_doc = doc_type

    total = sum(label_counts.values())

    confidence = (
        best_score / total
        if total > 0 else 0
    )

    return {
        "document_type": best_doc,
        "confidence": round(confidence, 4),
        "detected_labels": dict(label_counts)
    }