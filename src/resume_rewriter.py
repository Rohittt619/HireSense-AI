from src.ai_feedback import AIFeedback


class ResumeRewriter:

    def rewrite(
        self,
        resume,
        jd
    ):

        prompt = f"""

Rewrite this Resume professionally.

Resume

{resume}

Job Description

{jd}

"""

        return AIFeedback().ask(prompt)