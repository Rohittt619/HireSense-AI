from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


class ReportGenerator:

    @staticmethod
    def generate(
        filename,
        ats,
        similarity,
        skills,
        overall,
        feedback
    ):

        import os
        from pathlib import Path
        
        output_dir = Path(filename).parent
        os.makedirs(output_dir, exist_ok=True)

        styles = getSampleStyleSheet()

        doc = SimpleDocTemplate(filename)

        story = []

        story.append(
            Paragraph(
                "<b>HireSense AI Resume Analysis Report</b>",
                styles["Title"]
            )
        )

        story.append(Spacer(1, 20))

        story.append(
            Paragraph(
                f"<b>ATS Score:</b> {ats}%",
                styles["BodyText"]
            )
        )

        story.append(
            Paragraph(
                f"<b>Resume Match:</b> {similarity}%",
                styles["BodyText"]
            )
        )

        story.append(
            Paragraph(
                f"<b>Skill Match:</b> {skills['score']}%",
                styles["BodyText"]
            )
        )

        story.append(
            Paragraph(
                f"<b>Overall Score:</b> {overall}%",
                styles["BodyText"]
            )
        )

        story.append(Spacer(1, 20))

        story.append(
            Paragraph(
                "<b>AI Feedback</b>",
                styles["Heading2"]
            )
        )

        story.append(
            Paragraph(
                feedback.replace("\n", "<br/>"),
                styles["BodyText"]
            )
        )

        doc.build(story)