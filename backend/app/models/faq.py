from sqlalchemy import Column, Integer, String, Text
from app.database import Base


class FAQ(Base):
    __tablename__ = "faqs"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String(80), nullable=True)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    keywords = Column(String(255), nullable=True)
