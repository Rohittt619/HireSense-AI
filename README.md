# 📄 HireSense AI — Enterprise AI Resume Analyzer & ATS Optimizer

[![Python 3.11](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.58-red.svg)](https://streamlit.io/)
[![Google Gemini API](https://img.shields.io/badge/Google--Gemini-1.5--Flash-green.svg)](https://deepmind.google/technologies/gemini/)
[![OpenSource](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

**HireSense AI** is an enterprise-grade, AI-powered Resume Analyzer, ATS (Applicant Tracking System) Optimizer, and Career Assistant. Built with **Streamlit**, **Google Gemini 1.5 Flash API**, **PyMuPDF / pdfplumber**, and **Plotly**, it evaluates candidate resumes against target job descriptions, identifies skill gaps, analyzes metric density, generates custom interview questions, and exports tailored resumes directly to Microsoft Word (`.docx`).

---

## ✨ Enterprise Features

- 🎯 **Dynamic ATS Keyword Matching**: Parses Job Descriptions dynamically to score keyword density and section layout.
- ⚡ **Quantifiable Impact Metric Scoring**: Evaluates bullet points for metrics, percentages, dollar amounts, and strong action verbs.
- 📊 **Interactive Skill Gap Analysis**: Visualizes matched vs missing skills using Plotly charts.
- 🤖 **Structured Gemini 1.5 Flash AI Feedback**: Returns JSON-formatted AI audits covering strengths, weaknesses, and actionable suggestions.
- 📄 **Multi-Format Document Export**: Exports rewritten resumes, interview prep sheets, and cover letters directly to Microsoft Word (`.docx`) and PDF.
- 📜 **SQLite Audit History**: Automatically persists previous resume audit scores for tracking.

---

## 🛠️ Architecture & Tech Stack

```text
HireSense-AI/
├── app.py                         # Main Streamlit Entry Point
├── ui/
│   ├── home.py                    # Dashboard & Audit Interface
│   └── components.py              # Visual UI components
├── src/
│   ├── ai_feedback.py             # Google Gemini 1.5 Flash Integration (JSON Schema)
│   ├── ats.py                     # Dynamic ATS & Structural Scorer
│   ├── impact_analyzer.py         # Quantifiable Metric & Action Verb Scorer
│   ├── docx_generator.py          # Microsoft Word (.docx) Buffer Exporter
│   ├── parser.py                  # Dual PDF Extraction (pdfplumber + PyMuPDF)
│   ├── skills.py                  # Regex Word Boundary Skill Extractor
│   ├── similarity.py              # TF-IDF & Cosine Similarity Matcher
│   └── report_generator.py        # ReportLab PDF Generator
├── database/
│   └── db.py                      # SQLite Persistent Audit Storage
└── requirements.txt               # Pinned Python Dependencies
```

---

## 🚀 Quickstart Guide

### 1. Clone the Repository
```bash
git clone https://github.com/Rohittt619/HireSense-AI.git
cd HireSense-AI
```

### 2. Set Up Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure Gemini API Key
Create a `.env` file in the project root directory:
```env
GEMINI_API_KEY="your_google_gemini_api_key_here"
```

### 4. Launch Streamlit Application
```bash
streamlit run app.py
```
Open `http://localhost:8501` in your browser.

---

## 👤 Author
- **Developer**: Rohit Rathod
- **GitHub**: [https://github.com/Rohittt619](https://github.com/Rohittt619)
- **Portfolio**: [https://rohittt619.github.io/](https://rohittt619.github.io/)