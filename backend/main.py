# from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
# from sqlalchemy.orm import Session
# import shutil, os

# from backend.database import init_db, SessionLocal, Meeting
# from backend.models import MeetingResponse
# from backend.services.transcription import transcribe
# from backend.services.summarizer import generate_summary
# from backend.services.sentiment import analyze_sentiment
# from backend.services.topics import categorize_meeting
# from backend.services.search import index_meeting, semantic_search
# app = FastAPI(title="AI Meeting Intelligence API")
# init_db()

# UPLOAD_DIR = "Data/uploads"
# os.makedirs(UPLOAD_DIR, exist_ok=True)


# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# @app.get("/")
# def read_root():
#     return {"message": "AI Meeting Intelligence API is running 🚀"}


# @app.post("/upload", response_model=MeetingResponse)
# def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
#     if not file.filename:
#         raise HTTPException(status_code=400, detail="Uploaded file has no filename")

#     # Save uploaded file
#     file_path = os.path.join(UPLOAD_DIR, file.filename)
#     with open(file_path, "wb") as buffer:
#         shutil.copyfileobj(file.file, buffer)

#     # Run analysis pipeline
#     transcript = transcribe(file_path)
#     summary = generate_summary(transcript)
#     sentiment = analyze_sentiment(transcript)
#     topics = categorize_meeting(transcript)

#     # If file already exists, update instead of creating duplicate
#     existing = db.query(Meeting).filter(Meeting.filename == file.filename).first()
#     if existing:
#         existing.transcript = transcript  # type: ignore
#         existing.summary = summary        # type: ignore
#         existing.sentiment = sentiment    # type: ignore
#         existing.topics = topics          # type: ignore
#         db.commit()
#         db.refresh(existing)
#         return existing

#     # Else insert new record
#     meeting = Meeting(
#         filename=file.filename,
#         transcript=transcript,
#         summary=summary,
#         sentiment=sentiment,
#         topics=topics,
#     )
#     db.add(meeting)
#     db.commit()
#     db.refresh(meeting)
#     return meeting


# @app.get("/meetings/{meeting_id}", response_model=MeetingResponse)
# def get_meeting(meeting_id: int, db: Session = Depends(get_db)):
#     meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()
#     if not meeting:
#         raise HTTPException(status_code=404, detail=f"Meeting with ID {meeting_id} not found")
#     return meeting

# from backend.services.search import index_meeting, semantic_search

# @app.get("/search")
# def search_meetings(q: str, top_k: int = 3):
#     results = semantic_search(q, top_k)
#     if not results:
#         return {"message": "No relevant meetings found"}
#     return {"query": q, "results": results}

from fastapi import FastAPI, UploadFile, File, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import os, shutil

from backend.database import init_db, SessionLocal, Meeting
from backend.services.transcription import transcribe
from backend.services.summarizer import generate_summary
from backend.services.sentiment import analyze_sentiment
from backend.services.topics import categorize_meeting
from backend.services.search import index_meeting, semantic_search

# Init FastAPI
app = FastAPI(title="AI Meeting Intelligence")
init_db()

# Directories
UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Templates & static
templates = Jinja2Templates(directory="frontend/templates")
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db)):
    meetings = db.query(Meeting).all()
    return templates.TemplateResponse("index.html", {"request": request, "meetings": meetings})


@app.post("/upload", response_class=HTMLResponse)
def upload_file(request: Request, file: UploadFile = File(...), db: Session = Depends(get_db)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    transcript = transcribe(file_path)
    summary = generate_summary(transcript)
    sentiment = analyze_sentiment(transcript)
    topics = categorize_meeting(transcript)

    existing = db.query(Meeting).filter(Meeting.filename == file.filename).first()
    if existing:
        existing.transcript, existing.summary, existing.sentiment, existing.topics = transcript, summary, sentiment, topics
        db.commit()
        db.refresh(existing)
        index_meeting(existing)
        return templates.TemplateResponse("meeting.html", {"request": request, "meeting": existing})

    meeting = Meeting(filename=file.filename, transcript=transcript, summary=summary, sentiment=sentiment, topics=topics)
    db.add(meeting)
    db.commit()
    db.refresh(meeting)
    index_meeting(meeting)

    return templates.TemplateResponse("meeting.html", {"request": request, "meeting": meeting})


@app.get("/meetings/{meeting_id}", response_class=HTMLResponse)
def get_meeting(request: Request, meeting_id: int, db: Session = Depends(get_db)):
    meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()
    return templates.TemplateResponse("meeting.html", {"request": request, "meeting": meeting})


@app.get("/search", response_class=HTMLResponse)
def search_meetings(request: Request, q: str = None, db: Session = Depends(get_db)):
    results = semantic_search(q, top_k=5) if q else []
    return templates.TemplateResponse("search.html", {"request": request, "results": results, "query": q})
