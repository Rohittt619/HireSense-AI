import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))

from src.parser import ResumeParser
from src.ats import ATSScorer

resume = ResumeParser().parse("data/resumes/resume.pdf")

score = ATSScorer().score(resume)

print("="*50)
print("ATS SCORE :", score)
print("="*50)