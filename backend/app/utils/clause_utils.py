import re
import spacy

nlp = spacy.load("en_core_web_sm")

MIN_WORDS = 8
MAX_WORDS = 180

SECTION_PATTERN = re.compile(
    r"^\d+(\.\d+)*[\)\.]?\s+"
)

BULLET_PATTERN = re.compile(
    r"^\([a-zA-Z0-9]+\)"
)

def clean_clause(text):
    if text is None:
        return ""

    text = str(text)

    text = re.sub(r"\s+", " ", text)

    return text.strip()

def is_heading(line):
    line = clean_clause(line)

    if not line:
        return False

    # FULL CAPS headings
    if len(line.split()) <= 10 and line.isupper():
        return True

    # Numbered headings
    if re.match(r"^\d+(\.\d+)*\s+[A-Z]", line):
        return True

    # Title-style headings
    if (
        len(line.split()) <= 12
        and not line.endswith(".")
        and line[0].isupper()
    ):
        return True

    return False

def is_section_boundary(line):
    line = clean_clause(line)

    if not line:
        return False

    # 1. 1.1 2.3.1 etc.
    if SECTION_PATTERN.match(line):
        return True

    # (a) (b) (i)
    if BULLET_PATTERN.match(line):
        return True

    return False

def split_clauses(text):
    if text is None:
        return []

    text = str(text)

    text = text.replace("\r", "\n")

    raw_lines = text.split("\n")

    clauses = []
    current = ""

    for line in raw_lines:
        line = clean_clause(line)

        if not line:
            continue

        # Heading isolation
        if is_heading(line):
            if current.strip():
                clauses.append(current.strip())

            current = ""
            continue

        # Section boundary splitting
        if is_section_boundary(line):
            if current.strip():
                clauses.append(current.strip())

            current = line
            continue

        current += " " + line

        doc = nlp(current)

        sentences = list(doc.sents)

        word_count = len(current.split())

        # Semantic sentence splitting
        if len(sentences) >= 2 and word_count >= 25:
            clauses.append(current.strip())
            current = ""

        # Hard max size splitting
        elif word_count >= MAX_WORDS:
            clauses.append(current.strip())
            current = ""

    if current.strip():
        clauses.append(current.strip())

    # Cleanup
    cleaned = []

    for clause in clauses:
        clause = clean_clause(clause)

        if len(clause.split()) < MIN_WORDS:
            continue

        cleaned.append(clause)

    # Deduplicate
    cleaned = list(dict.fromkeys(cleaned))

    return cleaned