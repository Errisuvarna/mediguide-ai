from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.feedback import Feedback
from app.schemas.feedback import FeedbackCreate, FeedbackOut

router = APIRouter(prefix="/api/feedback", tags=["feedback"])


@router.post("", response_model=FeedbackOut, status_code=201)
def submit_feedback(payload: FeedbackCreate, db: Session = Depends(get_db)):
    fb = Feedback(name=payload.name, rating=payload.rating, comments=payload.comments)
    db.add(fb)
    db.commit()
    db.refresh(fb)
    return FeedbackOut(
        id=fb.id, name=fb.name, rating=fb.rating, comments=fb.comments,
        created_at=fb.created_at.isoformat(),
    )
