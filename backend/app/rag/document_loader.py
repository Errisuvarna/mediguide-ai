"""
Loads the raw knowledge-base documents (Markdown/plain text) from disk.

In the full spec this also covers PDF loading; since the generated
knowledge base ships as Markdown (easier to author/version and to grade),
loading is a simple directory walk. Swapping in real hospital PDFs later
only requires adding a PyPDF extraction branch here — the rest of the
RAG pipeline (chunking, embedding, retrieval) is unaffected.
"""
from dataclasses import dataclass
from pathlib import Path
from typing import List


@dataclass
class RawDocument:
    source_file: str
    text: str


def load_knowledge_base(directory: str) -> List[RawDocument]:
    docs: List[RawDocument] = []
    base = Path(directory)
    if not base.exists():
        return docs
    for path in sorted(base.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        docs.append(RawDocument(source_file=path.name, text=text))
    return docs
