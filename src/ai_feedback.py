from pathlib import Path
from dotenv import load_dotenv
import os
import google.generativeai as genai

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")


class AIFeedback:

    def __init__(self):

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("Gemini API Key not found.")

        genai.configure(api_key=api_key)

        self.model = genai.GenerativeModel("gemini-2.5-flash")

    def generate_feedback(self, resume_text, jd_text):

        prompt = f"""
You are an ATS Resume Expert.

Analyze this resume against the Job Description.

Return:

1. Overall ATS Score (/100)
2. Missing Skills
3. Strengths
4. Weaknesses
5. Resume Improvements
6. Interview Preparation Tips

Resume:
{resume_text}

Job Description:
{jd_text}
"""

        try:

            response = self.model.generate_content(prompt)

            return response.text

        except Exception:

            return """
## 🤖 AI Feedback Temporarily Unavailable

Gemini API quota has been exceeded.

Everything else in HireSense AI is working correctly.

Please wait one minute and try again.
"""