from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.database import Base


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    patient_name = Column(String(120), nullable=False)
    patient_contact = Column(String(30), nullable=True)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=True)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    scheduled_time = Column(DateTime, nullable=True)
    status = Column(String(20), default="pending")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
