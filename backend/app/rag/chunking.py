"""
Simple, dependency-free document chunker: splits Markdown documents on
headings first, then hard-wraps any oversized section by word count so
no chunk overwhelms the embedding model or the LLM context window.
"""
import re
from dataclasses import dataclass
from typing import List

from app.rag.document_loader import RawDocument

MAX_CHUNK_WORDS = 180
HEADING_RE = re.compile(r"^#{1,3}\s+.*$", re.MULTILINE)


@dataclass
class Chunk:
    source_file: str
    chunk_index: int
    content: str


def _split_by_words(text: str, max_words: int) -> List[str]:
    words = text.split()
    if len(words) <= max_words:
        return [text.strip()] if text.strip() else []
    return [
        " ".join(words[i:i + max_words]).strip()
        for i in range(0, len(words), max_words)
        if words[i:i + max_words]
    ]


def chunk_document(doc: RawDocument) -> List[Chunk]:
    sections = re.split(r"(?=^#{1,3}\s)", doc.text, flags=re.MULTILINE)
    sections = [s.strip() for s in sections if s.strip()]
    if not sections:
        sections = [doc.text]

    chunks: List[Chunk] = []
    idx = 0
    for section in sections:
        for piece in _split_by_words(section, MAX_CHUNK_WORDS):
            chunks.append(Chunk(source_file=doc.source_file, chunk_index=idx, content=piece))
            idx += 1
    return chunks


def chunk_all(docs: List[RawDocument]) -> List[Chunk]:
    all_chunks: List[Chunk] = []
    for doc in docs:
        all_chunks.extend(chunk_document(doc))
    return all_chunks
