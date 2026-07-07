import streamlit as st
from ui.home import show_home

st.set_page_config(
    page_title="HireSense AI",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

with st.sidebar:

    st.image(
        "https://cdn-icons-png.flaticon.com/512/3135/3135715.png",
        width=120
    )

    st.title("HireSense AI")

    st.write("---")

    st.success("AI Resume Analyzer")

    st.write("### Features")

    st.write("✅ ATS Score")

    st.write("✅ Resume Matching")

    st.write("✅ Skill Analysis")

    st.write("✅ AI Feedback")

    st.write("✅ Charts")

    st.write("✅ PDF Report")

    st.write("---")

    st.caption("Made with ❤️ by Rohit Rathod")

show_home()