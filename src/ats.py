import re


class ATSScorer:

    def calculate(self, resume_text, jd_text=None):

        score = 0

        checks = {
            "email": r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
            "phone": r"\+?\d[\d\s-]{8,}",
            "education": r"education|university|degree|bachelor|master",
            "experience": r"experience|work|internship|employment",
            "projects": r"project|portfolio|built|developed",
        }

        resume = resume_text.lower()

        # Structural sections check (50% of total score)
        for pattern in checks.values():
            if re.search(pattern, resume):
                score += (50 / len(checks))

        # Dynamic Job Description Keyword Match (50% of total score)
        if jd_text:
            jd_words = set(re.findall(r'\b[a-zA-Z]{3,}\b', jd_text.lower()))
            resume_words = set(re.findall(r'\b[a-zA-Z]{3,}\b', resume))
            
            stop_words = {'and', 'the', 'for', 'with', 'you', 'that', 'have', 'this', 'from', 'are', 'will', 'your'}
            jd_keywords = jd_words - stop_words
            
            if jd_keywords:
                matched = jd_keywords.intersection(resume_words)
                jd_score = (len(matched) / len(jd_keywords)) * 50
                score += jd_score

        return round(score, 2)