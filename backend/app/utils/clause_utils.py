import re

def split_clauses(text: str):
    # Normalize text
    text = re.sub(r'\r\n', '\n', text)

    # Step 1: Split by double newlines (paragraphs)
    chunks = re.split(r'\n\s*\n', text)

    clauses = []

    for chunk in chunks:
        chunk = chunk.strip()

        # Ignore very small chunks
        if len(chunk) < 40:
            continue

        # Further split long chunks by sentence
        if len(chunk) > 500:
            sentences = re.split(r'(?<=[.!?])\s+', chunk)
            clauses.extend([s.strip() for s in sentences if len(s) > 40])
        else:
            clauses.append(chunk)

    return clauses