from typing import Optional, List
from pydantic import BaseModel, ConfigDict


class DoctorOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    full_name: str
    department_id: int
    designation: Optional[str] = None
    qualification: Optional[str] = None
    consultation_fee: float = 0.0
    room_number: Optional[str] = None
    available_days: Optional[str] = None
    available_time: Optional[str] = None
    experience_years: int = 0
