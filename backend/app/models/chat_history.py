from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, DateTime
from app.database import Base


class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(64), index=True, nullable=False)
    role = Column(String(10), nullable=False)  # user | assistant
    message = Column(Text, nullable=False)
    language = Column(String(10), default="en")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
