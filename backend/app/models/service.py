from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    description = Column(Text, nullable=True)
    fee = Column(Float, default=0.0)
    location = Column(String(120), nullable=True)

    department = relationship("Department", back_populates="services")
