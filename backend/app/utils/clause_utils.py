import re
import spacy

nlp = spacy.load("en_core_web_sm")

def clean_clause(text):
    if not text:
        return ""

    text = re.sub(r"\s+", " ", str(text))
    return text.strip()

def is_heading(line):
    line = line.strip()

    if len(line.split()) <= 10 and line.isupper():
        return True

    if re.match(r"^\d+(\.\d+)*\s+[A-Z]", line):
        return True

    return False

def split_clauses(text):
    if not text:
        return []

    text = text.replace("\r", "\n")

    lines = text.split("\n")

    clauses = []
    current = ""

    for line in lines:
        line = clean_clause(line)

        if not line:
            continue

        if is_heading(line):
            if current:
                clauses.append(current.strip())

            current = line
            continue

        current += " " + line

        # split semantically using spaCy
        doc = nlp(current)

        if len(list(doc.sents)) >= 2 and len(current.split()) > 25:
            clauses.append(current.strip())
            current = ""

    if current:
        clauses.append(current.strip())

    # remove duplicates
    clauses = list(dict.fromkeys(clauses))

    # remove tiny fragments
    clauses = [
        c for c in clauses
        if len(c.split()) >= 8
    ]

    return clauses