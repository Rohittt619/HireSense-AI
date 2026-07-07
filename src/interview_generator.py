from src.ai_feedback import AIFeedback


class InterviewGenerator:

    def generate(
        self,
        resume,
        jd
    ):

        prompt = f"""

Generate interview questions.

Give

HR

Python

SQL

Machine Learning

Projects

Resume

{resume}

Job Description

{jd}

"""

        return AIFeedback().ask(prompt)