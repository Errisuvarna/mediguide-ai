from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from app.database import Base


class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    floor_number = Column(Integer, nullable=True)
    building_name = Column(String(120), nullable=True)
    contact_number = Column(String(30), nullable=True)
    office_hours = Column(String(120), nullable=True)
    avg_waiting_time_minutes = Column(Integer, default=15)
    keywords = Column(Text, nullable=True)  # comma-separated search keywords

    doctors = relationship("Doctor", back_populates="department")
    services = relationship("Service", back_populates="department")
