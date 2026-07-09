from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")


class AIFeedback:

    def __init__(self):

        api_key = os.getenv("GEMINI_API_KEY")

        st.write("API key found:", api_key is not None)
        st.write("API key length:", len(api_key) if api_key else 0)

        if not api_key:
            raise Exception("Gemini API Key not found.")

        genai.configure(api_key=api_key)

        self.model = genai.GenerativeModel("gemini-2.5-flash")

    def ask(self, prompt):

        try:

            response = self.model.generate_content(prompt)

            return response.text

        except Exception as e:

            return f"""
## Gemini API

{str(e)}

Everything else in HireSense AI still works.
"""

    def generate_feedback(
        self,
        resume,
        jd
    ):

        prompt = f"""

You are an ATS Resume Expert.

Analyze this Resume.

Give

Overall Score

Strengths

Weaknesses

Missing Skills

Suggestions

Resume

{resume}

Job Description

{jd}

"""

        return self.ask(prompt)