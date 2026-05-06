import re

def clean_clause(text):
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def is_heading(text):
    text = text.strip()

    if len(text.split()) <= 8 and text.isupper():
        return True

    if re.match(r"^\d+(\.\d+)*\s+[A-Z]", text):
        return True

    return False

def split_clauses(text):
    if not text:
        return []

    text = text.replace("\r", "\n")

    raw_parts = re.split(
        r"\n\s*\n|(?=\n\d+(\.\d+)*)",
        text
    )

    clauses = []
    current_clause = ""

    for part in raw_parts:
        part = clean_clause(part)

        if not part:
            continue

        if is_heading(part):
            if current_clause:
                clauses.append(current_clause.strip())

            current_clause = part
            continue

        if current_clause:
            current_clause += " " + part
        else:
            current_clause = part

        if len(current_clause.split()) >= 8:
            clauses.append(current_clause.strip())
            current_clause = ""

    if current_clause:
        clauses.append(current_clause.strip())

    clauses = list(dict.fromkeys(clauses))

    return clauses