from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai

# Load local .env (for VS Code)
ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")


class AIFeedback:

    def __init__(self):

        # 1. Streamlit Cloud Secret
        api_key = st.secrets.get("GEMINI_API_KEY", None)

        # 2. Local .env fallback
        if not api_key:
            api_key = os.getenv("GEMINI_API_KEY")

        # Debug
        st.write("API key found:", api_key is not None)
        st.write("API key length:", len(api_key) if api_key else 0)

        if not api_key:
            raise Exception(
                "Gemini API Key not found. Add GEMINI_API_KEY in Streamlit Secrets or .env"
            )

        genai.configure(api_key=api_key)

        self.model = genai.GenerativeModel(
            "gemini-2.5-flash"
        )

    def ask(self, prompt):

        st.write("🚀 Sending request to Gemini...")

        try:
            response = self.model.generate_content(prompt)

            st.write("✅ Gemini replied")

            return response.text

        except Exception as e:

            st.error(e)

            return f"""

        
## Gemini API Error

{str(e)}

Everything else in HireSense AI still works.
"""

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