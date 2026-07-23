import json
from src.ai_feedback import AIFeedback

class SalaryEstimator:
    """
    Uses Gemini AI to estimate market salary ranges and career trajectory 
    based on the candidate's resume and target job description.
    """

    @staticmethod
    def estimate(resume_text: str, jd_text: str) -> dict:
        prompt = f"""
You are a Tech Compensation Specialist and Senior Executive Recruiter.
Based on the candidate's resume and target job description, estimate current industry market salary ranges and career growth steps.

Return a JSON object with keys:
{{
    "job_title": "Junior Data Scientist",
    "estimated_salary_range_usd": "$75,000 - $95,000 / year",
    "estimated_salary_range_inr": "₹8,00,000 - ₹14,00,000 / year",
    "seniority_level": "Entry to Mid Level",
    "key_skills_for_salary_boost": ["AWS / Cloud Deployment", "PySpark", "Docker & MLOps"],
    "career_next_step": "Mid-Level Data Scientist / Machine Learning Engineer (2-3 years)"
}}

Candidate Resume:
{resume_text}

Job Description:
{jd_text}
"""
        raw_res = AIFeedback().ask(prompt, is_json=True)
        try:
            return json.loads(raw_res)
        except Exception:
            return {
                "job_title": "Target Role",
                "estimated_salary_range_usd": "$70,000 - $100,000 / year",
                "estimated_salary_range_inr": "₹7,00,000 - ₹12,00,000 / year",
                "seniority_level": "Junior Level",
                "key_skills_for_salary_boost": ["Cloud Architecture", "System Design"],
                "career_next_step": "Senior Specialist"
            }
