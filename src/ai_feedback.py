from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
import os
import json
import google.generativeai as genai

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

class AIFeedback:

    def __init__(self):
        api_key = None
        # Check Streamlit Cloud Secrets (GEMINI_API_KEY or GOOGLE_API_KEY)
        try:
            api_key = st.secrets.get("GEMINI_API_KEY") or st.secrets.get("GOOGLE_API_KEY")
        except Exception:
            pass

        # Check Local .env / OS environment variables
        if not api_key:
            api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

        if not api_key:
            raise Exception("Gemini API Key not found. Add GEMINI_API_KEY to Streamlit Secrets or .env.")

        genai.configure(api_key=api_key)

    def ask(self, prompt, is_json=False):
        # 1. Dynamic API Model Discovery
        try:
            available_models = [
                m.name for m in genai.list_models() 
                if "generateContent" in m.supported_generation_methods
            ]
            
            # Prioritize flash models, then pro models, then all others
            flash_models = [m for m in available_models if "flash" in m]
            pro_models = [m for m in available_models if "pro" in m]
            target_list = flash_models + pro_models + available_models

            for m_name in target_list:
                try:
                    gen_config = {"response_mime_type": "application/json"} if is_json else {}
                    m = genai.GenerativeModel(m_name, generation_config=gen_config)
                    res = m.generate_content(prompt)
                    if hasattr(res, "text") and res.text.strip():
                        return res.text
                except Exception:
                    continue
        except Exception:
            pass

        # 2. Direct Fallback List with 'models/' Prefix
        direct_models = [
            "models/gemini-1.5-flash",
            "models/gemini-1.5-pro",
            "models/gemini-1.0-pro",
            "gemini-1.5-flash-latest",
            "gemini-1.5-pro-latest"
        ]

        last_error = None
        for name in direct_models:
            try:
                gen_config = {"response_mime_type": "application/json"} if is_json else {}
                model = genai.GenerativeModel(name, generation_config=gen_config)
                response = model.generate_content(prompt)
                if hasattr(response, "text") and response.text.strip():
                    return response.text
            except Exception as e:
                last_error = e
                continue

        raise Exception(f"Gemini API Error: {str(last_error)}")

    def generate_feedback(self, resume, jd):
        prompt = f"""
You are an expert ATS Resume Auditor and Technical Recruiter.
Analyze the candidate resume against the target job description.

Return a JSON object with the exact keys:
{{
    "overall_ats_score": 85,
    "matching_skills": ["Python", "SQL", "Streamlit"],
    "missing_skills": ["Docker", "Kubernetes"],
    "resume_strengths": ["Clear project descriptions", "Relevant technical stack"],
    "resume_weaknesses": ["Lack of quantified impact metrics in experience section"],
    "actionable_suggestions": ["Quantify results with percentages", "Add missing keywords: Docker"],
    "final_verdict": "Strong candidate for initial phone screen."
}}

Resume Text:
{resume}

Job Description:
{jd}
"""
        raw_response = self.ask(prompt, is_json=True)
        try:
            parsed_json = json.loads(raw_response)
            return parsed_json
        except Exception:
            return {
                "overall_ats_score": 75,
                "matching_skills": [],
                "missing_skills": [],
                "resume_strengths": [raw_response],
                "resume_weaknesses": [],
                "actionable_suggestions": [],
                "final_verdict": "Parsed text feedback."
            }