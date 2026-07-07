import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))

from src.parser import ResumeParser

parser = ResumeParser()

text = parser.parse("data/resumes/resume.pdf")

print("=" * 60)
print(text[:5000])
print("=" * 60)