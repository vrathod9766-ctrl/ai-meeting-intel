🤖 #### AI Meeting Intelligence ####

An end-to-end AI-powered platform for meeting transcription, summarization, sentiment analysis, topic modeling, and semantic search.
Built with FastAPI, Whisper.cpp, Ollama LLMs, and ChromaDB.

🚀 Features

🎙 Audio/Video Ingestion – Supports .mp3, .wav, .mp4

📝 Transcription – High-fidelity speech-to-text with Whisper.cpp

📄 Summarization – Concise meeting summaries using Ollama LLMs

😊 Sentiment Analysis – Detect emotional tone of meetings

🏷 Topic Modeling – Auto-categorization with tags (e.g., Team Meeting, Client Call)

🔍 Semantic Search – Knowledge base powered by ChromaDB

📊 Dashboard (Bootstrap) – View transcripts, summaries, insights, and search results

⚡ Setup Instructions
Prerequisites

Python 3.10+

FFmpeg
 → for audio extraction

whisper.cpp
 → compiled binary

Ollama
 → for LLM inference (Llama2, Gemma, etc.)

Install
# Clone project
git clone https://github.com/yourname/ai-meeting-intel.git
cd ai-meeting-intel

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate      # Windows
source .venv/bin/activate   # Linux/Mac

# Install dependencies
pip install -r requirements.txt

Run
uvicorn backend.main:app --reload

📌 API Documentation

Base URL: http://127.0.0.1:8000

Endpoint	Method	Description
/	GET	Health check
/upload	POST	Upload audio/video file & run AI pipeline
/meetings/{id}	GET	Retrieve meeting details
/search?query=...	GET	Semantic search on transcripts

👉 Interactive API docs: http://127.0.0.1:8000/docs

🏗 Architecture

FastAPI → REST API backend

SQLite → Local database (can be swapped with PostgreSQL/MySQL)

Whisper.cpp → Transcription engine

Ollama LLMs → Summarization, sentiment, topic categorization

ChromaDB → Semantic search and knowledge base

Bootstrap + Jinja2 → Lightweight frontend

🔬 AI Pipeline

Upload file → .mp3/.wav/.mp4

Preprocessing → MP4 → WAV via FFmpeg

Transcription → Whisper.cpp → raw transcript

Summarization → Ollama LLM → concise summary

Sentiment → VADER + LLM → tone detection

Topics → LLM → category + tags

Indexing → Transcript stored in ChromaDB

Search → Semantic query over transcripts

⚠️ Challenges & Solutions

RAM limits on large LLMs → used smaller models (llama2:7b, gemma:2b)

Video ingestion → solved via FFmpeg audio extraction

Duplicate uploads → handled by updating existing DB entry

Newline formatting in browser → fixed using <br> for HTML rendering

✅ Error Handling

Unsupported file type → 400 Bad Request

File not found → 404 Not Found

Whisper/Ollama failures → 500 Internal Server Error

DB conflicts → update existing record instead of crash

📂 Project Structure
ai-meeting-intel/
│── backend/
│   │── main.py             # FastAPI entry point
│   │── models.py           # Pydantic & DB models
│   │── database.py         # SQLite setup
│   │── services/
│   │   │── transcription.py  # Whisper integration
│   │   │── summarizer.py     # LLM (Ollama) summary
│   │   │── sentiment.py      # Sentiment analysis
│   │   │── topics.py         # Topic modeling
│   │   │── search.py         # Semantic search (ChromaDB)
│   │── utils.py             # Helper functions
│── data/
│   │── uploads/            # Uploaded files
│   │── transcripts/        # Generated transcripts
│── requirements.txt
│── README.md

📊 Future Improvements

 Action item & task extraction

 Multi-speaker diarization

 Analytics dashboard with charts

 Docker deployment





 