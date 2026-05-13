import re
import spacy

nlp = spacy.load("en_core_web_sm")

MIN_WORDS = 8
MAX_WORDS = 160

SECTION_PATTERNS = [
    r"^\d+\.",
    r"^\d+\.\d+",
    r"^[A-Z][A-Z\s]{3,}$",
    r"^Section\s+\d+",
    r"^ARTICLE\s+[IVX]+",
]

LEGAL_CONNECTORS = [
    "provided that",
    "subject to",
    "including",
    "whereas",
    "however",
    "therefore",
    "further",
]

def clean_text(text):
    if not text:
        return ""

    text = str(text)

    text = text.replace("\r", "\n")

    text = re.sub(r"\s+", " ", text)

    return text.strip()

def is_heading(line):
    line = clean_text(line)

    if not line:
        return False

    for pattern in SECTION_PATTERNS:
        if re.match(pattern, line):
            return True

    if (
        len(line.split()) <= 10
        and line.isupper()
    ):
        return True

    return False

def should_merge(prev_clause, next_sentence):
    combined = (
        prev_clause.lower()
        + " "
        + next_sentence.lower()
    )

    for connector in LEGAL_CONNECTORS:
        if connector in combined:
            return True

    return False

def split_clauses(text):
    text = clean_text(text)

    if not text:
        return []

    raw_lines = text.split("\n")

    paragraphs = []

    current = ""

    for line in raw_lines:
        line = clean_text(line)

        if not line:
            continue

        if is_heading(line):
            if current.strip():
                paragraphs.append(current.strip())

            current = ""
            continue

        current += " " + line

    if current.strip():
        paragraphs.append(current.strip())

    clauses = []

    for para in paragraphs:

        doc = nlp(para)

        temp = ""

        for sent in doc.sents:

            sentence = sent.text.strip()

            if not sentence:
                continue

            if not temp:
                temp = sentence
                continue

            combined_words = len(
                (temp + " " + sentence).split()
            )

            if (
                combined_words <= MAX_WORDS
                and should_merge(temp, sentence)
            ):
                temp += " " + sentence

            else:
                clauses.append(temp.strip())
                temp = sentence

        if temp.strip():
            clauses.append(temp.strip())

    cleaned = []

    for clause in clauses:

        clause = clean_text(clause)

        word_count = len(clause.split())

        if word_count < MIN_WORDS:
            continue

        cleaned.append(clause)

    cleaned = list(dict.fromkeys(cleaned))

    return cleaned