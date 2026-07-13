from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    floor_id = Column(Integer, ForeignKey("floors.id"), nullable=False)
    room_number = Column(String(20), nullable=False)
    room_type = Column(String(60), nullable=True)
    department_name = Column(String(120), nullable=True)

    floor = relationship("Floor", back_populates="rooms")
