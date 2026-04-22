IMPORTANT_PHRASES = {
    "high_risk": [
        "terminate for convenience",
        "without prior notice",
        "sole discretion",
        "indemnify and hold harmless",
        "not liable for any damages"
    ],
    "medium_risk": [
        "late payment fee",
        "automatic renewal",
        "subject to change"
    ]
}

def generate_ngrams(tokens, n):
    return [' '.join(tokens[i:i+n]) for i in range(len(tokens)-n+1)]


def extract_ngrams(text):
    tokens = text.lower().split()

    bigrams = generate_ngrams(tokens, 2)
    trigrams = generate_ngrams(tokens, 3)

    return {
        "bigrams": bigrams,
        "trigrams": trigrams
    }

def detect_phrases(ngrams):
    detected = []

    for phrase in IMPORTANT_PHRASES["high_risk"]:
        if phrase in ngrams["bigrams"] or phrase in ngrams["trigrams"]:
            detected.append((phrase, "high"))

    for phrase in IMPORTANT_PHRASES["medium_risk"]:
        if phrase in ngrams["bigrams"] or phrase in ngrams["trigrams"]:
            detected.append((phrase, "medium"))

    return detected