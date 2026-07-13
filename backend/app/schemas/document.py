from typing import Optional
from pydantic import BaseModel, ConfigDict


class RequiredDocumentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    process_name: str
    document_name: str
    is_mandatory: str = "yes"
    notes: Optional[str] = None
