from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
import os
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
            raise Exception(
                "Gemini API Key not found. Add GEMINI_API_KEY to .env or Streamlit Secrets."
            )

        genai.configure(api_key=api_key)

        self.model = genai.GenerativeModel(
            "gemini-2.5-flash"
        )

    def ask(self, prompt):

        try:

            response = self.model.generate_content(prompt)

            if hasattr(response, "text"):
                return response.text

            return "No response returned from Gemini."

        except Exception as e:

            raise Exception(f"Gemini Error: {str(e)}")

    def generate_feedback(self, resume, jd):

        prompt = f"""
You are an ATS Resume Expert.

Analyze the following resume against the job description.

Return:

# Overall ATS Score (/100)

# Matching Skills

# Missing Skills

# Resume Strengths

# Resume Weaknesses

# Suggestions to Improve

# Final Verdict

Resume:

{resume}

Job Description:

{jd}
"""

        return self.ask(prompt)