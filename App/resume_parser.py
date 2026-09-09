# import os
# import io
# import multiprocessing as mp
# import pprint
# from spacy.matcher import Matcher
# import utils
# from nlp_loader import load_nlp


# class ResumeParser:
#     def __init__(
#         self,
#         resume,
#         skills_file=None,
#         custom_regex=None,
#         model_name="en_core_web_sm"  # ✅ Easily switch to transformer
#     ):
#         # ✅ Load NLP ONCE (cached)
#         self.nlp = load_nlp(model_name)
#         self.matcher = Matcher(self.nlp.vocab)

#         self.resume = resume
#         self.skills_file = skills_file
#         self.custom_regex = custom_regex

#         self.details = {
#             "name": None,
#             "email": None,
#             "mobile_number": None,
#             "skills": [],
#             "degree": None,
#             "no_of_pages": None,
#         }

#         self._parse_resume()

#     # ---------------- CORE PIPELINE ---------------- #

#     def _parse_resume(self):
#         ext = self._get_extension()
#         self.text_raw = utils.extract_text(self.resume, f".{ext}")
#         self.text_clean = " ".join(self.text_raw.split())

#         self.doc = self.nlp(self.text_clean)
#         self.noun_chunks = list(self.doc.noun_chunks)

#         self._extract_basic_details()

#     def _get_extension(self):
#         if isinstance(self.resume, io.BytesIO):
#             return self.resume.name.split(".")[-1]
#         return os.path.splitext(self.resume)[1].replace(".", "")

#     # ---------------- EXTRACTION ---------------- #

#     def _extract_basic_details(self):
#         try:
#             custom_entities = utils.extract_entities_wih_custom_model(self.doc)
#         except Exception:
#             custom_entities = {}

#         # Name
#         self.details["name"] = (
#             custom_entities.get("Name", [None])[0]
#             or utils.extract_name(self.doc, self.matcher)
#         )

#         # Email
#         self.details["email"] = utils.extract_email(self.text_clean)

#         # Mobile
#         self.details["mobile_number"] = utils.extract_mobile_number(
#             self.text_clean, self.custom_regex
#         )

#         # Skills
#         self.details["skills"] = utils.extract_skills(
#             self.doc, self.noun_chunks, self.skills_file
#         )

#         # Pages
#         self.details["no_of_pages"] = utils.get_number_of_pages(self.resume)

#         # Degree
#         self.details["degree"] = custom_entities.get("Degree")

#     # ---------------- PUBLIC API ---------------- #

#     def get_extracted_data(self):
#         return self.details


# # ---------------- MULTIPROCESSING ---------------- #

# def resume_result_wrapper(resume_path):
#     parser = ResumeParser(resume_path)
#     return parser.get_extracted_data()


# if __name__ == "__main__":
#     resumes = []
#     for root, _, filenames in os.walk("resumes"):
#         for filename in filenames:
#             resumes.append(os.path.join(root, filename))

#     with mp.Pool(mp.cpu_count()) as pool:
#         results = pool.map(resume_result_wrapper, resumes)

#     pprint.pprint(results)

import os
import io
import re
from pdfminer.high_level import extract_text
import nltk

nltk.download("stopwords")

class ResumeParser:
    def __init__(self, resume, skills_file=None, custom_regex=None):
        self.resume = resume
        self.skills_file = skills_file
        self.custom_regex = custom_regex

        self.details = {
            "name": "Candidate",
            "email": None,
            "mobile_number": None,
            "skills": [],
            "degree": None,
            "no_of_pages": 1,
        }

        self._parse_resume()

    def _parse_resume(self):
        text = extract_text(self.resume)
        self.text = " ".join(text.split())

        self.details["email"] = self._extract_email()
        self.details["mobile_number"] = self._extract_mobile()
        self.details["skills"] = self._extract_skills()
        self.details["no_of_pages"] = self.text.count("\f") + 1
        self.details["degree"] = self._extract_degree()

    def _extract_email(self):
        match = re.search(r"[\w\.-]+@[\w\.-]+", self.text)
        return match.group(0) if match else ""

    def _extract_mobile(self):
        match = re.search(r"\b\d{10}\b", self.text)
        return match.group(0) if match else ""

    def _extract_skills(self):
        SKILLS = [
            "python","java","c","c++","sql","html","css","javascript",
            "react","django","flask","machine learning","data science",
            "android","flutter","kotlin","nlp","deep learning"
        ]
        text = self.text.lower()
        return list(set(skill for skill in SKILLS if skill in text))

    def _extract_degree(self):
        degrees = ["b.tech", "bachelor", "master", "m.tech", "mba", "b.sc", "m.sc"]
        text = self.text.lower()
        for d in degrees:
            if d in text:
                return d.upper()
        return ""

    def get_extracted_data(self):
        return self.details
