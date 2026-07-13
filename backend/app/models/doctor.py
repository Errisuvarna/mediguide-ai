from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(120), nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)
    designation = Column(String(120), nullable=True)
    qualification = Column(String(160), nullable=True)
    consultation_fee = Column(Float, default=0.0)
    room_number = Column(String(20), nullable=True)
    available_days = Column(String(80), nullable=True)
    available_time = Column(String(60), nullable=True)
    experience_years = Column(Integer, default=0)

    department = relationship("Department", back_populates="doctors")
    specializations = relationship("DoctorSpecialization", back_populates="doctor")


class DoctorSpecialization(Base):
    __tablename__ = "doctor_specializations"

    id = Column(Integer, primary_key=True, index=True)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False)
    specialization = Column(String(120), nullable=False)

    doctor = relationship("Doctor", back_populates="specializations")
