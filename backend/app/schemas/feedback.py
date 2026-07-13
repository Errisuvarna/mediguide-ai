from typing import Optional
from pydantic import BaseModel, Field


class FeedbackCreate(BaseModel):
    name: Optional[str] = None
    rating: int = Field(ge=1, le=5)
    comments: Optional[str] = None


class FeedbackOut(FeedbackCreate):
    id: int
    created_at: str
