import fitz

def extract_text(pdf_path):
    text = ""

    try:
        doc = fitz.open(pdf_path)

        for page in doc:
            text += page.get_text()

        doc.close()

    except Exception as e:
        print("PDF extraction failed:", e)
        return None

    return text.strip()