from typing import Optional
from pydantic import BaseModel, ConfigDict


class HospitalMapPointOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    category: Optional[str] = None
    building_name: Optional[str] = None
    floor_number: Optional[int] = None
    x_coordinate: float
    y_coordinate: float
    description: Optional[str] = None
