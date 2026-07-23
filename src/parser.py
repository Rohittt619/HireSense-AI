import warnings
warnings.filterwarnings("ignore")

import fitz
import pdfplumber
from pathlib import Path

# Suppress PyMuPDF font descriptor warning messages in logs
try:
    fitz.TOOLS.mupdf_display_errors(False)
except Exception:
    pass

class ResumeParser:

    def __init__(self):
        pass

    def parse(self, file_path):
        file_path = Path(file_path)
        text = ""

        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception:
            text = ""

        if len(text.strip()) < 20:
            text = ""
            try:
                doc = fitz.open(file_path)
                for page in doc:
                    text += page.get_text()
                doc.close()
            except Exception:
                pass

        return text