from dotenv import load_dotenv
from pathlib import Path
import os

# Load the .env from the project root
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

print("ENV Loaded:", os.getenv("GEMINI_API_KEY"))