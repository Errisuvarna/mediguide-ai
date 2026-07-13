from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, Float
from app.database import Base


class AnalyticsEvent(Base):
    """One row per meaningful user interaction, used to power the dashboard."""
    __tablename__ = "analytics_events"

    id = Column(Integer, primary_key=True, index=True)
    event_type = Column(String(40), nullable=False)
    department = Column(String(120), nullable=True)
    language = Column(String(10), default="en")
    is_voice = Column(Integer, default=0)
    is_emergency = Column(Integer, default=0)
    response_time_ms = Column(Float, default=0.0)
    was_answered = Column(Integer, default=1)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)
