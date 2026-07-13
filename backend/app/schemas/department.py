from typing import Optional
from pydantic import BaseModel, ConfigDict


class DepartmentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    description: Optional[str] = None
    floor_number: Optional[int] = None
    building_name: Optional[str] = None
    contact_number: Optional[str] = None
    office_hours: Optional[str] = None
    avg_waiting_time_minutes: int = 15
    keywords: Optional[str] = None
