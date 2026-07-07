import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from src.parser import ResumeParser
from src.jd_parser import JDParser
from src.skills import SkillExtractor
from src.visualizer import Visualizer

resume = ResumeParser().parse("data/resumes/resume.pdf")

jd = JDParser().parse("data/job_descriptions/data_scientist.txt")

result = SkillExtractor().compare(resume, jd)

Visualizer.skill_chart(result)