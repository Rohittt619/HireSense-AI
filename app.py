import warnings
warnings.filterwarnings("ignore")

import sys
import os
from pathlib import Path

# Add project root directory to sys.path for Streamlit Cloud execution
ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# Pre-import core packages to populate sys.modules cleanly
import database.db
import src
import ui.home

import streamlit as st

st.set_page_config(
    page_title="HireSense AI",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

ui.home.show_home()