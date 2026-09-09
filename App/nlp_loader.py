import spacy
from functools import lru_cache

@lru_cache(maxsize=1)
def load_nlp(model_name: str = "en_core_web_sm"):
    """
    Loads spaCy model once per process (fast & safe).
    """
    return spacy.load(model_name)
