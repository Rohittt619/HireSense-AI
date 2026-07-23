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
from src.ats_redflags import ATSRedFlagAuditor
from src.salary_estimator import SalaryEstimator


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

    # Streamlit State Management: Triggers on Analyze Resume button
    analyze_clicked = st.button("🚀 Analyze Resume", use_container_width=True)

    if analyze_clicked:
        if uploaded_resume is None:
            st.error("Please upload a PDF resume.")
            return

        if not job_description.strip():
            st.error("Please paste a Job Description.")
            return

        with st.spinner("Analyzing resume, scoring ATS metrics & querying Gemini AI..."):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(uploaded_resume.read())
                resume_path = tmp.name

            resume_text = ResumeParser().parse(resume_path)

            similarity = SimilarityCalculator().calculate(resume_text, job_description)
            ats_score = ATSScorer().calculate(resume_text, job_description)
            skills = SkillExtractor().compare(resume_text, job_description)
            impact_data = ImpactAnalyzer.calculate_impact_score(resume_text)
            redflag_data = ATSRedFlagAuditor.audit(resume_text)

            overall = round((ats_score + similarity + skills["score"] + impact_data["impact_score"] + redflag_data["health_score"]) / 5, 2)

            ResumeDB().save(
                uploaded_resume.name,
                ats_score,
                similarity,
                skills["score"],
                overall
            )

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

            # Store results in st.session_state
            st.session_state["analyzed"] = True
            st.session_state["resume_text"] = resume_text
            st.session_state["job_description"] = job_description
            st.session_state["ats_score"] = ats_score
            st.session_state["similarity"] = similarity
            st.session_state["skills"] = skills
            st.session_state["impact_data"] = impact_data
            st.session_state["redflag_data"] = redflag_data
            st.session_state["overall"] = overall
            st.session_state["feedback"] = feedback

    # Render results if analyzed session state is active
    if st.session_state.get("analyzed"):
        resume_text = st.session_state["resume_text"]
        job_description = st.session_state["job_description"]
        ats_score = st.session_state["ats_score"]
        similarity = st.session_state["similarity"]
        skills = st.session_state["skills"]
        impact_data = st.session_state["impact_data"]
        redflag_data = st.session_state["redflag_data"]
        overall = st.session_state["overall"]
        feedback = st.session_state["feedback"]

        # PDF Report Download Button
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

        # Score Metrics Display
        col1, col2, col3, col4, col5, col6 = st.columns(6)
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
            st.metric("🛡️ Formatting", f"{redflag_data['health_score']}%")
            st.progress(int(min(redflag_data['health_score'], 100)))
        with col6:
            st.metric("⭐ Overall", f"{overall}%")
            st.progress(int(min(overall, 100)))

        st.divider()

        # Skill Chart
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

        # 1. ATS Red Flag & Formatting Audit Card
        with st.expander("🚩 ATS Red Flag & Formatting Audit", expanded=True):
            st.markdown(f"### 🛡️ Format Health Score: **{redflag_data['health_score']}/100**")
            st.caption(f"Total Resume Length: {redflag_data['word_count']} words")
            
            if redflag_data["red_flags"]:
                st.markdown("#### ❌ Critical ATS Red Flags Detected")
                for flag in redflag_data["red_flags"]:
                    st.error(f"• {flag}")
            else:
                st.success("🎉 Zero ATS formatting red flags detected!")
                
            st.markdown("#### ✅ Passed Format Checks")
            for check in redflag_data["passed_checks"]:
                st.success(f"• {check}")

        st.divider()

        # 2. AI Feedback Card
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

        # 3. AI Salary Estimator & Career Growth
        with st.expander("💰 AI Salary Estimator & Career Insights", expanded=False):
            if st.button("Estimate Market Salary & Growth Trajectory"):
                with st.spinner("Analyzing compensation benchmarks using Gemini AI..."):
                    st.session_state["salary_data"] = SalaryEstimator.estimate(resume_text, job_description)

            if st.session_state.get("salary_data"):
                sal = st.session_state["salary_data"]
                st.markdown(f"### 💼 Target Role: **{sal.get('job_title', 'Data Specialist')}** ({sal.get('seniority_level', 'Junior-Mid')})")
                
                col_s1, col_s2 = st.columns(2)
                with col_s1:
                    st.success(f"💵 **US Salary Range**: {sal.get('estimated_salary_range_usd', 'N/A')}")
                with col_s2:
                    st.success(f"🇮🇳 **India Salary Range**: {sal.get('estimated_salary_range_inr', 'N/A')}")

                st.markdown("#### 📈 Key Skills to Boost Your Compensation")
                for sk in sal.get("key_skills_for_salary_boost", []):
                    st.markdown(f"- **{sk}**")

                st.markdown(f"#### 🚀 Recommended Next Career Step: **{sal.get('career_next_step', 'Next Senior Role')}**")

        st.divider()

        # 4. AI Resume Rewriter Expander
        with st.expander("✨ AI Resume Rewriter & Word (.docx) Exporter", expanded=False):
            if st.button("Rewrite Resume for JD"):
                with st.spinner("Rewriting resume bullet points using Gemini AI..."):
                    st.session_state["rewritten"] = ResumeRewriter().rewrite(resume_text, job_description)

            if st.session_state.get("rewritten"):
                rewritten_text = st.session_state["rewritten"]
                st.write(rewritten_text)

                col_a, col_b = st.columns(2)
                with col_a:
                    st.download_button(
                        "⬇ Download (.txt)",
                        rewritten_text,
                        file_name="rewritten_resume.txt"
                    )
                with col_b:
                    docx_bytes = DocxGenerator.generate_docx_bytes("Rewritten Resume", rewritten_text)
                    st.download_button(
                        "📄 Download Microsoft Word (.docx)",
                        docx_bytes,
                        file_name="rewritten_resume.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )

        st.divider()

        # 5. AI Interview Questions Expander
        with st.expander("🎤 Tailored Interview Questions", expanded=False):
            if st.button("Generate Interview Questions"):
                with st.spinner("Generating tailored interview questions..."):
                    st.session_state["questions"] = InterviewGenerator().generate(resume_text, job_description)

            if st.session_state.get("questions"):
                q_text = st.session_state["questions"]
                st.write(q_text)

                col_q1, col_q2 = st.columns(2)
                with col_q1:
                    st.download_button(
                        "⬇ Download (.txt)",
                        q_text,
                        file_name="interview_questions.txt"
                    )
                with col_q2:
                    docx_q = DocxGenerator.generate_docx_bytes("Interview Preparation Questions", q_text)
                    st.download_button(
                        "📄 Download Word (.docx)",
                        docx_q,
                        file_name="interview_questions.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )

        st.divider()

        # 6. AI Cover Letter Expander
        with st.expander("📄 Tailored Cover Letter", expanded=False):
            if st.button("Generate Cover Letter"):
                with st.spinner("Drafting tailored cover letter using Gemini AI..."):
                    st.session_state["cover"] = CoverLetterGenerator().generate(resume_text, job_description)

            if st.session_state.get("cover"):
                c_text = st.session_state["cover"]
                st.write(c_text)

                col_c1, col_c2 = st.columns(2)
                with col_c1:
                    st.download_button(
                        "⬇ Download (.txt)",
                        c_text,
                        file_name="cover_letter.txt"
                    )
                with col_c2:
                    docx_c = DocxGenerator.generate_docx_bytes("Cover Letter", c_text)
                    st.download_button(
                        "📄 Download Word (.docx)",
                        docx_c,
                        file_name="cover_letter.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )