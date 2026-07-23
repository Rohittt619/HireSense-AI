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
        # Streamlit Cloud
        try:
            api_key = st.secrets.get("GEMINI_API_KEY")
        except Exception:
            pass

        # Local .env
        if not api_key:
            api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise Exception("Gemini API Key not found. Add GEMINI_API_KEY to .env or Streamlit Secrets.")

        genai.configure(api_key=api_key)

        # Production Gemini 1.5 Flash Model
        self.model = genai.GenerativeModel("gemini-1.5-flash")
        
        # Structured JSON Model
        self.json_model = genai.GenerativeModel(
            "gemini-1.5-flash",
            generation_config={"response_mime_type": "application/json"}
        )

    def ask(self, prompt, is_json=False):
        try:
            target_model = self.json_model if is_json else self.model
            response = target_model.generate_content(prompt)

            if hasattr(response, "text"):
                return response.text

            return "No response returned from Gemini."
        except Exception as e:
            raise Exception(f"Gemini Error: {str(e)}")

    def generate_feedback(self, resume, jd):
        prompt = f"""
You are an expert ATS Resume Auditor and Technical Recruiter.
Analyze the following candidate resume against the target job description.

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