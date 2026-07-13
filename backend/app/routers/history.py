from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.chat_history import ChatHistory
from app.schemas.chat import ChatHistoryItem

router = APIRouter(prefix="/api/history", tags=["history"])


@router.get("", response_model=List[ChatHistoryItem])
def get_history(session_id: str = Query(...), db: Session = Depends(get_db)):
    rows = (
        db.query(ChatHistory)
        .filter(ChatHistory.session_id == session_id)
        .order_by(ChatHistory.created_at.asc())
        .all()
    )
    return [
        ChatHistoryItem(
            role=r.role, message=r.message, language=r.language,
            created_at=r.created_at.isoformat(),
        )
        for r in rows
    ]
