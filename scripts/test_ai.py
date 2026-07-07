import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))

from src.parser import ResumeParser
from src.jd_parser import JDParser
from src.ai_feedback import AIFeedback


resume = ResumeParser().parse("data/resumes/resume.pdf")

jd = JDParser().parse("data/job_descriptions/data_scientist.txt")

feedback = AIFeedback().generate_feedback(resume, jd)

print(feedback)