import re

class ATSRedFlagAuditor:
    """
    Audits resume text for common ATS parsing red flags (missing contact info, 
    non-standard headers, word count issues, and formatting traps).
    """

    @staticmethod
    def audit(resume_text: str) -> dict:
        text_lower = resume_text.lower()
        word_count = len(re.findall(r'\b\w+\b', resume_text))
        
        red_flags = []
        passed_checks = []

        # 1. Contact Info Checks
        email_found = bool(re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", resume_text))
        phone_found = bool(re.search(r"\+?\d[\d\s-]{8,}", resume_text))
        linkedin_found = "linkedin.com" in text_lower or "github.com" in text_lower

        if email_found:
            passed_checks.append("Email address detected.")
        else:
            red_flags.append("Missing contact email address.")

        if phone_found:
            passed_checks.append("Phone number detected.")
        else:
            red_flags.append("Missing phone number.")

        if linkedin_found:
            passed_checks.append("LinkedIn / GitHub profile link detected.")
        else:
            red_flags.append("No LinkedIn or GitHub profile links found.")

        # 2. Section Header Checks
        has_education = bool(re.search(r"\beducation\b|\bdegree\b|\buniversity\b", text_lower))
        has_experience = bool(re.search(r"\bexperience\b|\bemployment\b|\bwork history\b|\binternship\b", text_lower))
        has_skills = bool(re.search(r"\bskills\b|\btechnologies\b|\bcompetencies\b", text_lower))
        has_projects = bool(re.search(r"\bprojects\b|\bportfolio\b|\bkey projects\b", text_lower))

        if has_education and has_experience and has_skills:
            passed_checks.append("Standard ATS section headers present (Education, Experience, Skills).")
        else:
            if not has_education:
                red_flags.append("Non-standard or missing Education section header.")
            if not has_experience:
                red_flags.append("Non-standard or missing Work Experience section header.")
            if not has_skills:
                red_flags.append("Non-standard or missing Skills section header.")

        # 3. Length & Word Count Check
        if 250 <= word_count <= 1000:
            passed_checks.append(f"Optimal resume length ({word_count} words).")
        elif word_count < 250:
            red_flags.append(f"Resume is too short ({word_count} words). Aim for 400–800 words.")
        else:
            red_flags.append(f"Resume is long ({word_count} words). Ensure it fits 1–2 pages cleanly.")

        # Overall Red Flag Health Score out of 100
        health_score = max(0, 100 - (len(red_flags) * 15))

        return {
            "health_score": health_score,
            "word_count": word_count,
            "red_flags": red_flags,
            "passed_checks": passed_checks
        }
