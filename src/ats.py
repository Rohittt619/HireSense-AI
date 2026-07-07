import re


class ATSScorer:

    def calculate(self, resume_text, jd_text):

        score = 0

        checks = {
            "email": r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
            "phone": r"\+?\d[\d\s-]{8,}",
            "python": r"python",
            "sql": r"sql",
            "machine learning": r"machine learning",
            "tensorflow": r"tensorflow",
            "docker": r"docker",
            "project": r"project",
            "education": r"education",
            "experience": r"experience|internship",
        }

        text = resume_text.lower()

        for pattern in checks.values():

            if re.search(pattern, text):

                score += 100 / len(checks)

        return round(score, 2)