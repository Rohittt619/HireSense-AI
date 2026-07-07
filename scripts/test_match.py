import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))

from src.parser import ResumeParser
from src.preprocessing import TextCleaner
from src.jd_parser import JDParser
from src.similarity import ResumeMatcher

resume = ResumeParser("data/resumes/resume.pdf")

resume_text = TextCleaner.clean(resume.extract_text())

jd = JDParser().parse("data/job_descriptions/data_scientist.txt")

score = ResumeMatcher().compare(resume_text, jd)

print(f"MATCH SCORE : {score}%")