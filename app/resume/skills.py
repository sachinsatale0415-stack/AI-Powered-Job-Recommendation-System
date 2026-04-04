import spacy

nlp = spacy.load("en_core_web_sm")

SKILLS_DB = [
    "python", "sql", "c", "c++", "java",
    "embedded c", "rtos", "microcontroller",
    "data analysis", "machine learning",
    "excel", "power bi", "tableau"
]

def extract_skills(text):
    text = text.lower()
    doc = nlp(text)

    extracted_skills = set()

    for skill in SKILLS_DB:
        if skill in text:
            extracted_skills.add(skill)

    for token in doc:
        if token.text in SKILLS_DB:
            extracted_skills.add(token.text)

    return list(extracted_skills)