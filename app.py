import sys
import os
from pathlib import Path

# Add project root, ui, and src directories to sys.path for Streamlit Cloud execution
ROOT_DIR = Path(__file__).resolve().parent
UI_DIR = ROOT_DIR / "ui"
SRC_DIR = ROOT_DIR / "src"

for p in [ROOT_DIR, UI_DIR, SRC_DIR]:
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

import streamlit as st
from home import show_home

st.set_page_config(
    page_title="HireSense AI",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

show_home()