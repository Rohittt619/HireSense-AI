import streamlit as st
import tempfile

from src.parser import ResumeParser
from src.skills import SkillExtractor
from src.similarity import SimilarityCalculator
from src.ats import ATSScorer
from src.ai_feedback import AIFeedback
from src.visualizer import Visualizer


def show_home():

    st.title("📄 HireSense AI")
    st.subheader("AI Resume Analyzer & ATS Optimizer")

    st.info("""
### 🚀 AI Powered Resume Intelligence

Upload your Resume and paste a Job Description to get:

- 📄 ATS Score
- 🎯 Resume Match
- 💡 Skill Match
- 🤖 AI Feedback
- 📊 Interactive Analytics
""")

    st.divider()

    uploaded_resume = st.file_uploader(
        "📄 Upload Resume (PDF)",
        type=["pdf"]
    )

    job_description = st.text_area(
        "💼 Paste Job Description",
        height=220
    )

    if st.button("🚀 Analyze Resume", use_container_width=True):

        if uploaded_resume is None:
            st.error("Please upload a resume.")
            return

        if not job_description.strip():
            st.error("Please paste a Job Description.")
            return

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:

            tmp.write(uploaded_resume.read())

            resume_path = tmp.name

        # ----------------------------
        # Resume Parsing
        # ----------------------------

        resume_text = ResumeParser().parse(resume_path)

        # ----------------------------
        # Similarity
        # ----------------------------

        similarity = SimilarityCalculator().calculate(
            resume_text,
            job_description
        )

        # ----------------------------
        # ATS Score
        # ----------------------------

        ats_score = ATSScorer().score(
            resume_text
        )

        # ----------------------------
        # Skills
        # ----------------------------

        skills = SkillExtractor().compare(
            resume_text,
            job_description
        )

        # ----------------------------
        # Gemini AI
        # ----------------------------

        feedback = AIFeedback().generate_feedback(
            resume_text,
            job_description
        )

        st.divider()

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "📄 ATS Score",
                f"{ats_score}%"
            )
            st.progress(int(ats_score))

        with col2:
            st.metric(
                "🎯 Resume Match",
                f"{similarity}%"
            )
            st.progress(int(similarity))

        with col3:
            st.metric(
                "💡 Skill Match",
                f"{skills['score']}%"
            )
            st.progress(int(skills["score"]))

        st.divider()

        st.subheader("📊 Overall Resume Analysis")

        overall = round(
            (ats_score + similarity + skills["score"]) / 3,
            2
        )

        st.metric(
            "Overall Score",
            f"{overall}%"
        )

        st.progress(int(overall))

        st.divider()

        st.subheader("📈 Resume Analytics")

        pie = Visualizer.pie_chart(skills)

        bar = Visualizer.score_chart(
            ats_score,
            similarity,
            skills["score"]
        )

        c1, c2 = st.columns(2)

        with c1:
            st.plotly_chart(
                pie,
                use_container_width=True
            )

        with c2:
            st.plotly_chart(
                bar,
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
                st.success("No missing skills!")

        st.divider()

        st.subheader("🤖 AI Resume Feedback")

        st.write(feedback)