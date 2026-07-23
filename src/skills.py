import json
from pathlib import Path


class SkillExtractor:

    def __init__(self):

        skills_file = Path("data/skills/skills.json")

        with open(skills_file, "r", encoding="utf-8") as f:
            self.skills = json.load(f)

    def extract(self, text):

        import re
        text_lower = text.lower()
        found = []

        for skill in self.skills:
            pattern = r"\b" + re.escape(skill.lower()) + r"\b"
            if re.search(pattern, text_lower):
                found.append(skill)

        return sorted(list(set(found)))

    def compare(self, resume_text, jd_text):

        resume_skills = self.extract(resume_text)

        jd_skills = self.extract(jd_text)

        matched = sorted(list(set(resume_skills) & set(jd_skills)))

        missing = sorted(list(set(jd_skills) - set(resume_skills)))

        score = 0

        if len(jd_skills):

            score = round(len(matched) / len(jd_skills) * 100, 2)

        return {
            "resume_skills": resume_skills,
            "jd_skills": jd_skills,
            "matched": matched,
            "missing": missing,
            "score": score
        }