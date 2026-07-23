import sys
import os
from pathlib import Path

# Add project root directory to sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

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
from src.impact_analyzer import ImpactAnalyzer
from src.docx_generator import DocxGenerator


def show_home():

    st.sidebar.title("🚀 HireSense AI")

    page = st.sidebar.radio(
        "Navigation",
        ["Dashboard", "History"]
    )

    if page == "History":
        st.title("📜 Resume Audit History")
        history = ResumeDB().fetch()
        if history:
            st.dataframe(history, use_container_width=True)
        else:
            st.info("No audit history available.")
        return

    st.title("📄 HireSense AI")
    st.subheader("Enterprise AI Resume Analyzer & ATS Optimizer")
    st.divider()

    uploaded_resume = st.file_uploader("Upload Resume", type=["pdf"])
    job_description = st.text_area("Paste Job Description", height=220)

    if not st.button("🚀 Analyze Resume", use_container_width=True):
        return

    if uploaded_resume is None:
        st.error("Please upload a PDF resume.")
        return

    if not job_description.strip():
        st.error("Please paste a Job Description.")
        return

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_resume.read())
        resume_path = tmp.name

    resume_text = ResumeParser().parse(resume_path)

    # 1. Similarity & ATS Scores
    similarity = SimilarityCalculator().calculate(resume_text, job_description)
    ats_score = ATSScorer().calculate(resume_text, job_description)
    skills = SkillExtractor().compare(resume_text, job_description)
    impact_data = ImpactAnalyzer.calculate_impact_score(resume_text)

    overall = round((ats_score + similarity + skills["score"] + impact_data["impact_score"]) / 4, 2)

    # Save to SQLite Database
    ResumeDB().save(
        uploaded_resume.name,
        ats_score,
        similarity,
        skills["score"],
        overall
    )

    # 2. Structured AI Feedback (Gemini JSON)
    try:
        feedback = AIFeedback().generate_feedback(resume_text, job_description)
    except Exception as e:
        st.error(f"❌ Gemini Error: {e}")
        feedback = {
            "overall_ats_score": ats_score,
            "matching_skills": skills["matched"],
            "missing_skills": skills["missing"],
            "resume_strengths": ["Clear format"],
            "resume_weaknesses": ["Missing metrics"],
            "actionable_suggestions": ["Add numbers to bullet points"],
            "final_verdict": "Manual review required."
        }

    # 3. PDF Report Generation
    try:
        feedback_str = str(feedback) if isinstance(feedback, dict) else feedback
        ReportGenerator.generate("reports/report.pdf", ats_score, similarity, skills, overall, feedback_str)

        with open("reports/report.pdf", "rb") as pdf:
            st.download_button(
                "📥 Download PDF Executive Report",
                pdf,
                file_name="HireSense_Report.pdf",
                mime="application/pdf"
            )
    except Exception as e:
        st.error(f"❌ PDF Generation Error: {e}")

    st.divider()

    # Metrics Display
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric("📄 ATS", f"{ats_score}%")
        st.progress(int(min(ats_score, 100)))

    with col2:
        st.metric("🎯 Match", f"{similarity}%")
        st.progress(int(min(similarity, 100)))

    with col3:
        st.metric("💡 Skills", f"{skills['score']}%")
        st.progress(int(min(skills["score"], 100)))

    with col4:
        st.metric("⚡ Impact", f"{impact_data['impact_score']}%")
        st.progress(int(min(impact_data['impact_score'], 100)))

    with col5:
        st.metric("⭐ Overall", f"{overall}%")
        st.progress(int(min(overall, 100)))

    st.divider()

    # Skill Visualization
    st.subheader("📊 Skill Gap Analysis")
    chart = Visualizer.chart(skills)
    st.plotly_chart(chart, use_container_width=True)

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

    # AI Structured Feedback Cards
    with st.expander("🤖 AI Resume Audit & Verdict", expanded=True):
        if isinstance(feedback, dict):
            st.markdown(f"### 📋 Final Verdict: **{feedback.get('final_verdict', 'Reviewed')}**")
            
            st.markdown("#### 💪 Resume Strengths")
            for strength in feedback.get("resume_strengths", []):
                st.markdown(f"- {strength}")
                
            st.markdown("#### ⚠️ Resume Weaknesses")
            for weakness in feedback.get("resume_weaknesses", []):
                st.markdown(f"- {weakness}")
                
            st.markdown("#### 💡 Actionable Improvement Suggestions")
            for sug in feedback.get("actionable_suggestions", []):
                st.markdown(f"- {sug}")
        else:
            st.write(feedback)

    st.divider()

    # Rewriter + Word DOCX Export
    with st.expander("✨ AI Resume Rewriter & Word (.docx) Exporter"):
        if st.button("Rewrite Resume for JD"):
            rewritten = ResumeRewriter().rewrite(resume_text, job_description)
            st.write(rewritten)

            col_a, col_b = st.columns(2)
            with col_a:
                st.download_button(
                    "⬇ Download (.txt)",
                    rewritten,
                    file_name="rewritten_resume.txt"
                )
            with col_b:
                docx_bytes = DocxGenerator.generate_docx_bytes("Rewritten Resume", rewritten)
                st.download_button(
                    "📄 Download Microsoft Word (.docx)",
                    docx_bytes,
                    file_name="rewritten_resume.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )

    st.divider()

    # Interview Generator
    with st.expander("🎤 Tailored Interview Questions"):
        if st.button("Generate Interview Questions"):
            questions = InterviewGenerator().generate(resume_text, job_description)
            st.write(questions)
            
            docx_q = DocxGenerator.generate_docx_bytes("Interview Preparation Questions", questions)
            st.download_button(
                "📄 Download Word (.docx)",
                docx_q,
                file_name="interview_questions.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )

    st.divider()

    # Cover Letter Generator
    with st.expander("📄 Tailored Cover Letter"):
        if st.button("Generate Cover Letter"):
            cover = CoverLetterGenerator().generate(resume_text, job_description)
            st.write(cover)
            
            docx_c = DocxGenerator.generate_docx_bytes("Cover Letter", cover)
            st.download_button(
                "📄 Download Word (.docx)",
                docx_c,
                file_name="cover_letter.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )