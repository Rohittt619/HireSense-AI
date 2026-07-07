import streamlit as st
from ui.home import show_home

st.set_page_config(
    page_title="HireSense AI",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

show_home()