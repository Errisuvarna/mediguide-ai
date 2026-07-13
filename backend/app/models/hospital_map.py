from sqlalchemy import Column, Integer, String, Float, Text
from app.database import Base


class HospitalMapPoint(Base):
    __tablename__ = "hospital_map_points"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    category = Column(String(60), nullable=True)
    building_name = Column(String(120), nullable=True)
    floor_number = Column(Integer, nullable=True)
    x_coordinate = Column(Float, nullable=False)
    y_coordinate = Column(Float, nullable=False)
    description = Column(Text, nullable=True)
