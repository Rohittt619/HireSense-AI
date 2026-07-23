<div align="center">

# 📄 HireSense AI — Enterprise AI Resume Analyzer & ATS Optimizer

[![Python 3.11](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.58-red.svg)](https://streamlit.io/)
[![Google Gemini API](https://img.shields.io/badge/Google--Gemini-1.5--Flash-green.svg)](https://deepmind.google/technologies/gemini/)
[![OpenSource](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

**HireSense AI** is an enterprise-grade, AI-powered Resume Analyzer, ATS (Applicant Tracking System) Optimizer, and Career Assistant. Built with **Streamlit**, **Google Gemini 1.5 Flash API**, **PyMuPDF / pdfplumber**, **python-docx**, and **Plotly**, it evaluates candidate resumes against target job descriptions, identifies skill gaps, analyzes metric density, generates custom interview questions, and exports tailored resumes directly to Microsoft Word (`.docx`).

</div>

---

# 📷 Screenshots

### 🏠 Dashboard Overview
![Dashboard](assets/dashboard.png)

---

### 📊 Interactive Skill Gap Analysis
![Skill Analysis](assets/skill_analysis.png)

---

### 🤖 Gemini AI Resume Audit Feedback
![AI Feedback](assets/ai_feedback.png)

---

# 🧠 How It Works

```text
Upload Resume
        │
        ▼
Upload Job Description
        │
        ▼
Dual PDF Parsing (pdfplumber + PyMuPDF)
        │
        ▼
Skill Extraction & Metric Impact Scoring
        │
        ▼
Dynamic ATS & Keyword Score Calculation
        │
        ▼
Structured Gemini 1.5 Flash AI Feedback
        │
        ▼
PDF Report & Word (.docx) Export Generation
```

---

# ✨ Core Features & Modules

### 📄 Dual PDF Parser
- Reads PDF Resumes reliably using `pdfplumber` with fallback to `PyMuPDF` (`fitz`).
- Cleans formatting and extracts text cleanly across multi-column layouts.

### 🎯 Dynamic ATS & Keyword Scorer
- Dynamic Keyword Match based on uploaded Job Description.
- Evaluates structural section presence (Education, Experience, Projects, Contact Info).

### ⚡ Quantifiable Impact Metric Scorer
- Scans bullet points for metrics (`%`, `$`, scale), percentages, and strong action verbs (`built`, `engineered`, `optimized`).
- Calculates a dedicated **Impact Score** to boost real ATS ranking.

### 🤖 Gemini 1.5 Flash AI Feedback
- Google Gemini 1.5 Flash outputs structured JSON audits covering:
  - Strengths & Weaknesses
  - Actionable Improvement Suggestions
  - Final Candidate Verdict

### 📊 Interactive Skill Gap Analysis
- Visualizes Matched Skills vs Missing Skills using interactive Plotly charts.

### ✍ AI Resume Rewriter & Word (.docx) Exporter
- Rewrites resume bullet points to align with the target Job Description.
- Exports formatted resumes directly to Microsoft Word (`.docx`) and `.txt`.

### 🎤 AI Interview Question Generator
- Creates tailored interview prep questions based on the candidate's resume and skill gaps.
- Exports questions directly to Microsoft Word (`.docx`).

### 📄 AI Cover Letter Generator
- Automatically generates a personalized cover letter matching the uploaded resume and job description.
- Exports cover letters to Microsoft Word (`.docx`).

### 📥 Executive PDF Report
- Generates downloadable professional PDF report including ATS Score, Skill Match, and AI Audit.

---

# 🛠️ Architecture & Tech Stack

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

# ⚙ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/Rohittt619/HireSense-AI.git
cd HireSense-AI
```

### 2. Create Virtual Environment
```bash
python -m venv venv
```

### 3. Activate Virtual Environment
- **Windows**:
  ```bash
  venv\Scripts\activate
  ```
- **macOS / Linux**:
  ```bash
  source venv/bin/activate
  ```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env` file in the root directory:
```env
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
```

---

# ▶ Run Application

```bash
streamlit run app.py
```
Open `http://localhost:8501` in your browser.

---

# 🚀 Future Improvements

- Resume Ranking System for Recruiters
- Multiple Resume Comparison Side-by-Side
- LinkedIn Profile Import & Analyzer
- AI Mock Interview Voice Agent
- Multi-language Resume Analysis

---

# 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create a new branch (`git checkout -b feature-name`)
3. Commit changes (`git commit -m "Added new feature"`)
4. Push changes (`git push origin feature-name`)
5. Create a Pull Request

---

# 👨‍💻 Author

## Rohit Rathod

🎓 **B.Tech (Data Science)**  
💼 **Aspiring Data Analyst | Data Engineer | Data Scientist**

- **GitHub**: [https://github.com/Rohittt619](https://github.com/Rohittt619)
- **LinkedIn**: [https://www.linkedin.com/in/rohit-rathod-19442a228/](https://www.linkedin.com/in/rohit-rathod-19442a228/)
- **Portfolio**: [https://rohittt619.github.io/](https://rohittt619.github.io/)

---

# 📜 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

<div align="center">

⭐ If you found this project useful, don't forget to star the repository!

Made with ❤️ by Rohit Rathod

</div>