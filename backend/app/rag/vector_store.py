"""
Minimal in-memory vector store (cosine similarity over a NumPy matrix).

This stands in for ChromaDB: same conceptual role (store chunk
embeddings, similarity-search them), zero external service to run,
which keeps the hackathon build to `uvicorn app.main:app` with no
extra infrastructure. Swapping in real ChromaDB later means replacing
just this file — `retriever.py` only calls `.add()` and `.search()`.
"""
from dataclasses import dataclass, field
from typing import List, Tuple

import numpy as np

from app.rag.chunking import Chunk
from app.rag.embeddings import EmbeddingModel


@dataclass
class VectorStore:
    chunks: List[Chunk] = field(default_factory=list)
    matrix: np.ndarray = field(default_factory=lambda: np.zeros((0, 0)))

    def add(self, chunks: List[Chunk]) -> None:
        if not chunks:
            return
        model = EmbeddingModel.instance()
        texts = [c.content for c in chunks]
        embeddings = model.encode(texts)
        self.chunks = list(chunks)
        self.matrix = embeddings

    def search(self, query: str, top_k: int = 4) -> List[Tuple[Chunk, float]]:
        if not self.chunks or self.matrix.shape[0] == 0:
            return []
        model = EmbeddingModel.instance()
        query_vec = model.encode([query])[0]

        matrix_norms = np.linalg.norm(self.matrix, axis=1)
        matrix_norms[matrix_norms == 0] = 1.0
        query_norm = np.linalg.norm(query_vec) or 1.0

        sims = (self.matrix @ query_vec) / (matrix_norms * query_norm)
        top_indices = np.argsort(-sims)[:top_k]
        return [(self.chunks[i], float(sims[i])) for i in top_indices if sims[i] > 0]


_store = VectorStore()


def get_vector_store() -> VectorStore:
    return _store
