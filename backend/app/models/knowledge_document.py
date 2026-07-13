from sqlalchemy import Column, Integer, String, Text
from app.database import Base


class KnowledgeDocument(Base):
    """Metadata for chunks loaded into the in-memory vector store (see app/rag)."""
    __tablename__ = "knowledge_documents"

    id = Column(Integer, primary_key=True, index=True)
    source_file = Column(String(150), nullable=False)
    chunk_index = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
