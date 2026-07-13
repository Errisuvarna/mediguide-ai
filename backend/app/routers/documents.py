from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.document import RequiredDocument
from app.schemas.document import RequiredDocumentOut

router = APIRouter(prefix="/api/documents", tags=["documents"])


@router.get("", response_model=List[RequiredDocumentOut])
def list_documents(process_name: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(RequiredDocument)
    if process_name:
        query = query.filter(RequiredDocument.process_name.ilike(f"%{process_name}%"))
    return query.order_by(RequiredDocument.process_name).all()
