import re


class ATSScorer:

    def calculate(self, resume_text, jd_text=None):

        score = 0

        checks = {
            "email": r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
            "phone": r"\+?\d[\d\s-]{8,}",
            "education": r"education",
            "experience": r"experience|internship",
            "projects": r"project",
            "skills": r"python|sql|machine learning|tensorflow|docker"
        }

        resume = resume_text.lower()

        for pattern in checks.values():

            if re.search(pattern, resume):
                score += 100 / len(checks)

        return round(score, 2)