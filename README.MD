<div align="center">

# 🤖 AI Processing Studio

### *An elegant, high-performance document processing pipeline that transforms PDFs into beautiful, AI-generated Word summaries in real time.*

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python Version" />
  <img src="https://img.shields.io/badge/FastAPI-v0.100+-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI Framework" />
  <img src="https://img.shields.io/badge/Groq-LLaMA_3.3-F55036?style=for-the-badge&logo=rocket&logoColor=white" alt="Groq LLaMA" />
  <img src="https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker Ready" />
</p>

---

[🚀 Quick Setup](#-getting-started) • [🛠️ Tech Stack](#%EF%B8%8F-tech-stack) • [📜 License](#-license)

</div>

<br />

## ✨ Key Features

| Feature | Description |
| :--- | :--- |
| 📄 **Smart PDF Upload** | Accept PDFs up to **50MB** with real-time validation. |
| 🤖 **AI-Powered Summaries** | Generate dense, structured summaries powered by **Groq LLaMA 3.3 70B**. |
| ⚡ **Async Background Workers** | Processes files completely out-of-band via **3 concurrent worker pools**. |
| 📊 **Real-time Pipeline Tracker** | Watch progress visualizers in real time `(Extract ➔ Summarize ➔ DOCX ➔ Done)`. |
| 🧹 **Auto Storage Protection**| Auto-cleans raw PDFs after text extraction to protect your server storage. |
| 📥 **Professional Export** | Instantly download beautifully formatted, production-ready `.docx` files. |
| 🌙 **Modern Glassmorphic UI** | Responsive, dark-mode first design with smooth micro-animations. |

<br />

## 🚀 Getting Started

### 📋 Prerequisites
* **Python 3.11+** installed
* A free **[Groq API Key](https://console.groq.com/keys)**

### 💻 Installation

Get the application up and running locally in just a few commands:

```bash
# 1. Clone the repository
git clone https://github.com/rutviksatav/ai-processing-studio.git
cd ai-processing-studio

# 2. Setup your virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# 3. Install packages
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env and paste your GROQ_API_KEY=gsk_...

# 5. Launch the application!
uvicorn app.main:app --reload
```

> 🎯 **Next Step:** Open **[http://127.0.0.1:8000/frontend/index.html](http://127.0.0.1:8000/frontend/index.html)** in your browser to start processing your documents.

<br />

## 🛠️ Tech Stack

* **Backend Framework:** [FastAPI](https://fastapi.tiangolo.com/) (Asynchronous python)
* **AI Engine:** [Groq Cloud SDK](https://groq.com/) (LLaMA 3.3 70B model)
* **Database:** SQLite with [SQLAlchemy Async](https://docs.sqlalchemy.org/) & `aiosqlite`
* **File Processing:** `pypdf` (Text extraction) & `python-docx` (Document writer)
* **Frontend:** Modern Vanilla HTML5 / CSS3 (CSS Custom properties, Grid, Flexbox) / Javascript ES6

<br />

## 📜 License

Distributed under the MIT License. Created with ❤️ by **[Rutvik Satav](https://github.com/rutviksatav)**.
