import re

def split_clauses(text: str):
    if not text:
        return []

    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text)

    # 🔹 Split on legal clause boundaries
    clauses = re.split(
        r'(?:(?:\n|\r)|\.\s+|;\s+|\bWHEREAS\b|\bNOW, THEREFORE\b|\bSection\s+\d+)',
        text,
        flags=re.IGNORECASE
    )

    # 🔹 Clean + filter
    cleaned = []
    for clause in clauses:
        clause = clause.strip()

        # remove very short junk
        if len(clause) > 40:
            cleaned.append(clause)

    return cleaned