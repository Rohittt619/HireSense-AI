from src.ai_feedback import AIFeedback


class CoverLetterGenerator:

    def generate(
        self,
        resume,
        jd
    ):

        prompt = f"""

Write a professional Cover Letter.

Resume

{resume}

Job Description

{jd}

"""

        return AIFeedback().ask(prompt)