# Data Handling

## Data Collection
Since this is a hackathon build without access to a real hospital's
records, `dataset/generate_dataset.py` produces realistic **synthetic**
data for every required table: departments, doctors, services,
procedures, required documents, buildings, floors, rooms, FAQs, and
hospital map coordinates. Values are drawn from curated real-world-style
templates (Indian hospital department names, common consultation fees,
realistic doctor availability patterns) rather than pure random noise,
so the dataset is usable for meaningful demos.

## Data Cleaning & Validation
- Every generated row is written through Python's typed dict structures,
  so column presence/type is guaranteed at generation time (no missing
  fields, no type mismatches).
- Foreign keys (e.g. `doctor.department_id`, `room.floor_id`) are only
  ever assigned from IDs that were generated in the same run, so
  referential integrity holds by construction.
- SQLAlchemy column constraints (`nullable=False`, `String` length caps)
  provide a second validation layer when the seed script loads the data.

## Synthetic Data Generation
`generate_dataset.py` uses a fixed random seed (42) for reproducibility.
It outputs three formats per table for grading flexibility:
- **CSV** — for spreadsheet review / data-handling criteria
- **JSON** — consumed by `backend/app/seed/seed_db.py` to populate SQLite
- **SQL** (`seed_data.sql`) — a portable INSERT-statement seed file that
  works against SQLite or PostgreSQL directly

Total: **648 records** across 10 tables (exceeds the 500-record minimum).

## Preprocessing for RAG
Knowledge-base Markdown documents (`knowledge_base/*.md`) go through:
1. **Document loading** — read from disk (`document_loader.py`)
2. **Chunking** — split on Markdown headings, then hard-wrapped to a
   180-word max per chunk (`chunking.py`)
3. **Embedding** — Sentence-Transformers (`all-MiniLM-L6-v2`), with an
   automatic local TF-IDF fallback if the model can't be downloaded
   (`embeddings.py`)
4. **Indexing** — stored in an in-memory cosine-similarity vector store,
   rebuilt on every app startup (`vector_store.py`, `retriever.py`)
