from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Floor(Base):
    __tablename__ = "floors"

    id = Column(Integer, primary_key=True, index=True)
    building_id = Column(Integer, ForeignKey("buildings.id"), nullable=False)
    floor_number = Column(Integer, nullable=False)
    label = Column(String(80), nullable=True)

    building = relationship("Building", back_populates="floors")
    rooms = relationship("Room", back_populates="floor")
