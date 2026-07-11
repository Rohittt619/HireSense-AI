import streamlit as st
import tempfile

from database.db import ResumeDB
from src.report_generator import ReportGenerator
from src.parser import ResumeParser
from src.similarity import SimilarityCalculator
from src.skills import SkillExtractor
from src.ats import ATSScorer
from src.ai_feedback import AIFeedback

from src.resume_rewriter import ResumeRewriter
from src.interview_generator import InterviewGenerator
from src.cover_letter import CoverLetterGenerator

from src.visualizer import Visualizer


def show_home():

    st.sidebar.title("🚀 HireSense AI")

    page = st.sidebar.radio(

        "Navigation",

        [

            "Dashboard",

            "History"

        ]

    )

    if page == "History":

        st.title("📜 Resume History")

        history = ResumeDB().fetch()

        if history:

            st.dataframe(

                history,

                use_container_width=True

            )

        else:

            st.info("No history available.")

        return

    st.title("📄 HireSense AI")

    st.subheader("AI Resume Analyzer & ATS Optimizer")

    st.divider()

    uploaded_resume = st.file_uploader(

        "Upload Resume",

        type=["pdf"]

    )

    job_description = st.text_area(

        "Paste Job Description",

        height=220

    )

    if not st.button(

        "🚀 Analyze Resume",

        use_container_width=True

    ):

        return

    if uploaded_resume is None:

        st.error("Upload Resume.")

        return

    if not job_description.strip():

        st.error("Paste Job Description.")

        return

    with tempfile.NamedTemporaryFile(

        delete=False,

        suffix=".pdf"

    ) as tmp:

        tmp.write(

            uploaded_resume.read()

        )

        resume_path = tmp.name

    resume_text = ResumeParser().parse(

        resume_path

    )

    similarity = SimilarityCalculator().calculate(

        resume_text,

        job_description

    )

    ats_score = ATSScorer().calculate(

        resume_text,
        
        job_description
        
    )

    skills = SkillExtractor().compare(

        resume_text,

        job_description

    )

    overall = round(

        (

            ats_score +

            similarity +

            skills["score"]

        ) / 3,

        2

    )

    ResumeDB().save(

        uploaded_resume.name,

        ats_score,

        similarity,

        skills["score"],

        overall

    )

    # ---------- AI Feedback ----------
    try:
        feedback = AIFeedback().generate_feedback(
            resume_text,
            job_description
        )
    except Exception as e:
        st.error(f"❌ Gemini Error:\n{e}")
        feedback = "AI Feedback unavailable."

    # ---------- PDF Report ----------
    try:
        ReportGenerator.generate(
            "reports/report.pdf",
            ats_score,
            similarity,
            skills,
            overall,
            feedback
        )

        with open("reports/report.pdf", "rb") as pdf:
            st.download_button(
                "📥 Download PDF Report",
                pdf,
                file_name="HireSense_Report.pdf",
                mime="application/pdf"
            )

    except Exception as e:
        st.error(f"❌ PDF Generation Error:\n{e}")

    st.divider()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("📄 ATS", f"{ats_score}%")
        st.progress(int(ats_score))

    with col2:
        st.metric("🎯 Match", f"{similarity}%")
        st.progress(int(similarity))

    with col3:
        st.metric("💡 Skills", f"{skills['score']}%")
        st.progress(int(skills["score"]))

    with col4:
        st.metric("⭐ Overall", f"{overall}%")
        st.progress(int(overall))

    st.divider()

    st.subheader("📊 Skill Analysis")

    chart = Visualizer.chart(skills)

    st.plotly_chart(
        chart,
        use_container_width=True
    )

    st.divider()

    left, right = st.columns(2)

    with left:
        st.subheader("✅ Matched Skills")

        if skills["matched"]:
            for skill in skills["matched"]:
                st.success(skill)
        else:
            st.info("No matched skills found.")

    with right:
        st.subheader("❌ Missing Skills")

        if skills["missing"]:
            for skill in skills["missing"]:
                st.error(skill)
        else:
            st.success("No missing skills 🎉")

    st.divider()

    with st.expander("🤖 AI Resume Feedback", expanded=True):
        st.write(feedback)

    st.divider()

    with st.expander("✨ AI Resume Rewriter"):

        if st.button("Rewrite Resume"):

            rewritten = ResumeRewriter().rewrite(
                resume_text,
                job_description
            )

            st.write(rewritten)

            st.download_button(
                "⬇ Download Rewritten Resume",
                rewritten,
                file_name="rewritten_resume.txt"
            )

    st.divider()

    with st.expander("🎤 Interview Questions"):

        if st.button("Generate Interview Questions"):

            questions = InterviewGenerator().generate(
                resume_text,
                job_description
            )

            st.write(questions)

            st.download_button(
                "⬇ Download Questions",
                questions,
                file_name="interview_questions.txt"
            )

    st.divider()

    with st.expander("📄 Cover Letter"):

        if st.button("Generate Cover Letter"):

            cover = CoverLetterGenerator().generate(
                resume_text,
                job_description
            )

            st.write(cover)

            st.download_button(
                "⬇ Download Cover Letter",
                cover,
                file_name="cover_letter.txt"
            )