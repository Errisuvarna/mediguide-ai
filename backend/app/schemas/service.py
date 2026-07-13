from typing import Optional
from pydantic import BaseModel, ConfigDict


class ServiceOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    department_id: Optional[int] = None
    description: Optional[str] = None
    fee: float = 0.0
    location: Optional[str] = None
