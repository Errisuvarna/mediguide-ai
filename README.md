# 🏥 MediGuide AI — Intelligent Voice-Based Hospital Navigation & Patient Assistance System

MediGuide AI is a digital hospital receptionist: patients, visitors, and
elderly users can type or speak a question — in English, Hindi, or
Telugu — and get instant guidance on departments, doctors, rooms,
registration, billing, insurance, admission, laboratory, pharmacy, and
emergency directions.

**This system does not diagnose disease, prescribe medicine, or replace
a doctor.** It is strictly a navigation and administrative assistant.

## Architecture

```
User → React (Vite + TS + Tailwind) → FastAPI → RAG pipeline
       (Sentence-Transformers embeddings → in-memory vector store →
        Gemini API) → Response
```

See [`docs/architecture.md`](docs/architecture.md) for full diagrams,
[`docs/folder_structure.md`](docs/folder_structure.md) for the repo
layout, and [`docs/data_handling.md`](docs/data_handling.md) for the
dataset methodology.

## Tech Stack

| Layer | Choice |
|---|---|
| Frontend | React, TypeScript, Vite, Tailwind CSS, React Router, Axios, Recharts |
| Backend | FastAPI, SQLAlchemy, Pydantic, JWT auth |
| Database | SQLite by default (swap `DATABASE_URL` for PostgreSQL with zero code changes) |
| Vector store | In-memory NumPy cosine-similarity store (swap-compatible with ChromaDB) |
| Embeddings | Sentence-Transformers `all-MiniLM-L6-v2`, auto-fallback to local TF-IDF |
| LLM | Google Gemini API (auto-fallback to best-matching KB chunk if no API key) |
| Voice | Web Speech API (STT) + SpeechSynthesis API (TTS) |

> **Why SQLite + in-memory vectors instead of PostgreSQL + ChromaDB?**
> This build intentionally trades managed infra for a zero-dependency
> local run — see the note at the bottom of `docs/architecture.md`.
> Both are drop-in replaceable later.

## Quick Start

### Backend
```bash
cd backend
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```
On first run, the backend automatically creates the SQLite database,
seeds it from `dataset/*.json` (648 records), and builds the RAG vector
index from `knowledge_base/*.md`. API docs: http://localhost:8000/docs

### Frontend
```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```
App runs at http://localhost:5173 and proxies `/api` to the backend.

### Regenerating the dataset (optional)
```bash
cd dataset
python generate_dataset.py
```

### Running with Docker Compose
```bash
docker compose up --build
```
Frontend: http://localhost:5173 · Backend: http://localhost:8000

## Testing

```bash
# Backend
cd backend && pytest

# Frontend
cd frontend && npm test
```

## REST API Summary

| Method | Path | Purpose |
|---|---|---|
| POST | `/api/chat` | RAG-powered chat (+ emergency detection) |
| POST | `/api/auth/login` | Admin/staff login (JWT) |
| POST | `/api/auth/register` | Create a staff/admin account |
| GET | `/api/departments` | List/search departments |
| GET | `/api/doctors` | List/search/filter doctors |
| GET | `/api/services` | List hospital services |
| GET | `/api/documents` | Required-documents checklist |
| GET | `/api/hospital-map` | Map coordinates |
| GET | `/api/analytics` | Dashboard summary + charts |
| POST | `/api/feedback` | Submit patient feedback |
| GET | `/api/history` | Chat history for a session |

Full interactive docs (Swagger UI) at `/docs` once the backend is running.

## Deployment

- **Frontend** → Vercel (`npm run build`, output `dist/`)
- **Backend** → Render / any Docker host (`backend/Dockerfile`)
- **Database** → ships as SQLite by default; point `DATABASE_URL` at a
  managed Postgres instance (e.g. Supabase) for production with no code
  changes

See [`docs/architecture.md`](docs/architecture.md) for the deployment
diagram.

## Project Structure

See [`docs/folder_structure.md`](docs/folder_structure.md).

## Important Note

MediGuide AI is a **navigation and administrative assistant only**. It
never diagnoses conditions, never recommends medicines or dosages, and
always defers medical questions to hospital doctors and nurses. For any
message containing emergency-indicating language (chest pain, severe
bleeding, unconsciousness, etc.), the system immediately directs the
user to the Emergency Department rather than answering conversationally.
