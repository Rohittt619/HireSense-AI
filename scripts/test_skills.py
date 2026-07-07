import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from src.parser import ResumeParser
from src.jd_parser import JDParser
from src.skills import SkillExtractor

resume = ResumeParser().parse("data/resumes/resume.pdf")

jd = JDParser().parse("data/job_descriptions/data_scientist.txt")

result = SkillExtractor().compare(resume, jd)

print("\nResume Skills")
print(result["resume_skills"])

print("\nJD Skills")
print(result["jd_skills"])

print("\nMatched Skills")
print(result["matched"])

print("\nMissing Skills")
print(result["missing"])

print("\nSkill Match:", result["score"], "%")