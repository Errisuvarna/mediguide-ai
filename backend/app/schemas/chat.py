from typing import Optional, List
from pydantic import BaseModel


class ChatRequest(BaseModel):
    session_id: str
    message: str
    language: str = "en"          # en | hi | te
    is_voice: bool = False


class SourceChunk(BaseModel):
    source_file: str
    snippet: str


class ChatResponse(BaseModel):
    session_id: str
    reply: str
    department_matched: Optional[str] = None
    is_emergency: bool = False
    sources: List[SourceChunk] = []
    response_time_ms: float = 0.0


class ChatHistoryItem(BaseModel):
    role: str
    message: str
    language: str
    created_at: str
