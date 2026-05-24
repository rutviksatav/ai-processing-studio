<div align="center">

# 🤖 AI Processing Studio

**Upload PDFs, get AI-powered summaries as downloadable Word documents.**

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Groq](https://img.shields.io/badge/Groq-LLaMA_3.3_70B-F55036?style=for-the-badge)](https://groq.com)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com)

</div>

---

## Features

- 📄 **PDF Upload** — Accepts PDFs up to 50MB
- 🤖 **AI Summarization** — Powered by Groq's LLaMA 3.3 70B model
- ⚡ **Async Queue** — 3 concurrent background workers
- 📊 **Live Progress** — Real-time pipeline stepper (Extract → Summarize → Generate → Done)
- 📥 **DOCX Download** — Professional Word document output

---

## Getting Started

### Prerequisites

- Python 3.11+
- [Groq API Key](https://console.groq.com/keys) (free)

### Setup

```bash
git clone https://github.com/rutviksatav/ai-processing-studio.git
cd ai-processing-studio

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt

cp .env.example .env
# Add your GROQ_API_KEY in .env

uvicorn app.main:app --reload
```

Open **http://127.0.0.1:8000/frontend/index.html**


## Tech Stack

**Backend:** FastAPI, SQLAlchemy (async), aiosqlite, Pydantic
**AI:** Groq SDK (LLaMA 3.3 70B Versatile)
**Documents:** pypdf, python-docx
**Frontend:** Vanilla HTML/CSS/JS

---

## License

MIT — [Rutvik Satav](https://github.com/rutviksatav)
