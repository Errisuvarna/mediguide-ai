from sqlalchemy import Column, Integer, String, Float, Text
from app.database import Base


class Procedure(Base):
    __tablename__ = "procedures"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    category = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)
    estimated_cost = Column(Float, default=0.0)
    prep_instructions = Column(Text, nullable=True)
