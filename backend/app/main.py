"""
MediGuide AI - FastAPI application entrypoint.

Run locally:
    uvicorn app.main:app --reload
"""
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import init_db
from app.seed.seed_db import seed as seed_database
from app.rag.retriever import build_index
from app.routers import (
    auth, departments, doctors, services, documents,
    hospital_map, feedback, history, chat, analytics,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mediguide")

app = FastAPI(
    title=settings.APP_NAME,
    description="Intelligent voice-based hospital navigation & patient assistance system.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_ORIGIN, "http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(departments.router)
app.include_router(doctors.router)
app.include_router(services.router)
app.include_router(documents.router)
app.include_router(hospital_map.router)
app.include_router(feedback.router)
app.include_router(history.router)
app.include_router(chat.router)
app.include_router(analytics.router)


@app.on_event("startup")
def on_startup() -> None:
    init_db()
    seed_database()
    chunk_count = build_index()
    logger.info("MediGuide AI backend ready. %d knowledge-base chunks indexed.", chunk_count)


@app.get("/")
def root():
    return {"status": "ok", "service": settings.APP_NAME}


@app.get("/api/health")
def health():
    return {"status": "healthy"}
