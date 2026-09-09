import re
from pathlib import Path
from pdfminer.high_level import extract_text as pdf_extract_text

EMAIL_REGEX = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")
PHONE_REGEX = re.compile(r"\+?\d[\d\s\-]{8,15}\d")


# ---------------- FILE TEXT EXTRACTION ---------------- #

def extract_text(file, ext):
    ext = ext.lower()

    if ext == ".pdf":
        return pdf_extract_text(file)

    if ext in [".txt"]:
        return Path(file).read_text(errors="ignore")

    raise ValueError(f"Unsupported file type: {ext}")


# ---------------- BASIC EXTRACTORS ---------------- #

def extract_email(text):
    match = EMAIL_REGEX.search(text)
    return match.group(0) if match else None


def extract_mobile_number(text, custom_regex=None):
    regex = custom_regex or PHONE_REGEX
    match = regex.search(text)
    return match.group(0) if match else None


def extract_name(doc, matcher=None):
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text
    return None


def extract_skills(doc, noun_chunks, skills_file=None):
    skills = set()

    COMMON_SKILLS = {
        "python", "java", "sql", "machine learning", "data analysis",
        "flutter", "dart", "react", "node", "aws", "docker"
    }

    for chunk in noun_chunks:
        text = chunk.text.lower()
        if text in COMMON_SKILLS:
            skills.add(chunk.text)

    return list(skills)


def extract_entities_wih_custom_model(doc):
    entities = {}
    for ent in doc.ents:
        entities.setdefault(ent.label_, []).append(ent.text)
    return entities


def get_number_of_pages(file):
    try:
        import fitz  # PyMuPDF
        doc = fitz.open(file)
        return doc.page_count
    except Exception:
        return None


