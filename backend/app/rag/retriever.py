"""
Ties document loading -> chunking -> embedding -> vector store together,
and exposes a single retrieve(query) used by the chat endpoint.
"""
import logging
from pathlib import Path
from typing import List, Tuple

from app.rag.document_loader import load_knowledge_base
from app.rag.chunking import chunk_all, Chunk
from app.rag.vector_store import get_vector_store
from app.config import settings

logger = logging.getLogger(__name__)

KNOWLEDGE_BASE_DIR = str(Path(__file__).resolve().parents[3] / "knowledge_base")


def build_index(knowledge_base_dir: str = KNOWLEDGE_BASE_DIR) -> int:
    """Loads + chunks + embeds the knowledge base into the in-memory store.
    Called once at application startup. Returns number of chunks indexed."""
    docs = load_knowledge_base(knowledge_base_dir)
    chunks = chunk_all(docs)
    store = get_vector_store()
    store.add(chunks)
    logger.info("RAG index built: %d documents -> %d chunks", len(docs), len(chunks))
    return len(chunks)


def retrieve(query: str, top_k: int | None = None) -> List[Tuple[Chunk, float]]:
    store = get_vector_store()
    return store.search(query, top_k=top_k or settings.TOP_K_RESULTS)
