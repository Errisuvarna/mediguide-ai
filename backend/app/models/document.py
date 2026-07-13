from sqlalchemy import Column, Integer, String, Text
from app.database import Base


class RequiredDocument(Base):
    __tablename__ = "required_documents"

    id = Column(Integer, primary_key=True, index=True)
    process_name = Column(String(120), nullable=False)
    document_name = Column(String(150), nullable=False)
    is_mandatory = Column(String(10), default="yes")
    notes = Column(Text, nullable=True)
