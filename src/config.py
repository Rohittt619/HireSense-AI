from pathlib import Path

# Project Root
ROOT_DIR = Path(__file__).resolve().parent.parent

# Data folders
DATA_DIR = ROOT_DIR / "data"

RESUME_DIR = DATA_DIR / "resumes"
JOB_DIR = DATA_DIR / "jobs"

# Outputs
OUTPUT_DIR = ROOT_DIR / "outputs"

# Models
MODEL_DIR = ROOT_DIR / "models"

# Reports
REPORT_DIR = ROOT_DIR / "reports"

# Assets
ASSET_DIR = ROOT_DIR / "assets"

# Create folders automatically

for folder in [
    RESUME_DIR,
    JOB_DIR,
    OUTPUT_DIR,
    MODEL_DIR,
    REPORT_DIR,
]:
    folder.mkdir(parents=True, exist_ok=True)