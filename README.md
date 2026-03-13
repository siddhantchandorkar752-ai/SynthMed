<div align="center">

# SynthMed

### Medical Report AI Assistant

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-LLaMA_3.3_70B-F55036?style=for-the-badge)
![Streamlit](https://img.shields.io/badge/Streamlit-1.40-FF4B4B?style=for-the-badge&logo=streamlit)
![PyMuPDF](https://img.shields.io/badge/PyMuPDF-1.24-00897B?style=for-the-badge)

**Upload any medical report PDF. Get instant AI-powered clinical insights, diagnosis analysis, risk identification, patient timelines, and multi-report comparisons.**

[Live Demo](#) · [Report Bug](https://github.com/siddhantchandorkar752-ai/SynthMed/issues)

</div>

---

## The Problem

Medical reports are dense, complex, and written for clinicians — not patients. A patient receives a 10-page report filled with medical jargon and has no idea what it means, what risks it implies, or what questions to ask their doctor.

**SynthMed solves this.** It reads any medical PDF and gives you instant, plain-English clinical insights powered by LLaMA 3.3 70B running on Groq.

---

## Features

| Feature | Description |
|---------|-------------|
| Report Summary | Plain-English overview of the entire report |
| Diagnosis Insights | Deep analysis of all diagnoses, test results, and lab values |
| Risk Factors | Identifies health risks rated LOW / MEDIUM / HIGH |
| Medications Review | Lists all drugs, dosages, and interactions |
| Patient Timeline | Chronological view of all medical events with severity colors |
| Multi-Report Comparison | Upload 2 PDFs and get a diff of clinical changes |
| Natural Language Q&A | Ask anything about the report in plain English |
| PDF Export | Download any analysis as a PDF |
| Session History | All analyses tracked in sidebar during session |

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| LLM | LLaMA 3.3 70B via Groq API |
| PDF Parsing | PyMuPDF (fitz) |
| Dashboard | Streamlit |
| Markdown Rendering | Custom regex renderer |
| PDF Export | PyMuPDF |

---

## Getting Started
```bash
git clone https://github.com/siddhantchandorkar752-ai/SynthMed.git
cd SynthMed
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Add your Groq API key to .env
streamlit run app.py
```

Get your free Groq API key at [console.groq.com](https://console.groq.com/keys)

---

## What I Learned

- Prompt engineering for structured clinical output from LLMs
- Building custom markdown-to-HTML renderers for Streamlit
- PDF text extraction and processing with PyMuPDF
- Designing production-grade medical AI interfaces with accessibility in mind
- Multi-document comparison using LLM context windows

---

## Why This Stands Out

Most AI projects call an API and display raw text. SynthMed goes further — it parses, structures, color-codes severity, builds timelines, compares documents, and exports everything. It is the kind of tool a hospital would actually deploy.

---

<div align="center">
Built by <a href="https://github.com/siddhantchandorkar752-ai">Siddhant Chandorkar</a>
</div>