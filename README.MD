# AI Processing Studio

An async document processing pipeline that uploads PDFs, extracts text, generates AI-powered summaries using Groq (LLaMA 3.3), and produces downloadable Word documents.

![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?logo=fastapi&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-LLaMA_3.3-orange)

## Features

- **PDF Upload & Processing** — Upload PDFs up to 50MB
- **Async Job Queue** — Configurable concurrent workers process jobs in the background
- **Real-time Status Tracking** — Live pipeline progress (Extract → Summarize → Generate DOCX)
- **AI Summarization** — Powered by Groq's LLaMA 3.3 70B model
- **DOCX Export** — Download professional Word document summaries
- **Crash Recovery** — Incomplete jobs are automatically re-enqueued on server restart
- **Auto Cleanup** — Uploaded PDFs are deleted after text extraction to save storage

## Architecture

```
Frontend (Vanilla JS) → FastAPI REST API → Async Queue → Workers
                                              ↓
                                    PDF Extract → LLM Summary → DOCX Generation
                                              ↓
                                         SQLite DB (job tracking)
```

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | FastAPI, SQLAlchemy (async), aiosqlite |
| AI | Groq API (LLaMA 3.3 70B Versatile) |
| Frontend | Vanilla HTML/CSS/JS |
| Database | SQLite |
| Document Processing | pypdf, python-docx |

## Getting Started

### Prerequisites

- Python 3.11+
- A [Groq API key](https://console.groq.com/keys)

### Local Setup

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/scheduler_app.git
cd scheduler_app

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your GROQ_API_KEY

# Run the application
uvicorn app.main:app --reload
```

Open **http://127.0.0.1:8000/frontend/index.html** in your browser.

### Docker

```bash
docker build -t ai-processing-studio .
docker run -p 8000:8000 -e GROQ_API_KEY=your_key_here ai-processing-studio
```

## Deployment (Render)

1. Push this repo to GitHub
2. Go to [render.com](https://render.com) → **New Web Service**
3. Connect your GitHub repo
4. Settings will auto-configure from `render.yaml`
5. Add your `GROQ_API_KEY` in the Render dashboard → Environment

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/jobs` | Upload a PDF file for processing |
| `GET` | `/jobs` | List all jobs with status |
| `GET` | `/jobs/{job_id}/download` | Download the generated DOCX summary |

## Project Structure

```
scheduler_app/
├── app/
│   ├── api/          # REST API routes
│   ├── core/         # Config & logging
│   ├── db/           # Database models & init
│   ├── queue/        # Async job queue & workers
│   ├── repositories/ # Data access layer
│   ├── schemas/      # Pydantic schemas & enums
│   ├── services/     # PDF, LLM, file processing
│   └── main.py       # FastAPI app entry point
├── frontend/         # Static HTML/CSS/JS frontend
├── Dockerfile
├── render.yaml
└── requirements.txt
```

## License

MIT
