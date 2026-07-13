from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.service import Service
from app.schemas.service import ServiceOut

router = APIRouter(prefix="/api/services", tags=["services"])


@router.get("", response_model=List[ServiceOut])
def list_services(department_id: Optional[int] = None, db: Session = Depends(get_db)):
    query = db.query(Service)
    if department_id:
        query = query.filter(Service.department_id == department_id)
    return query.order_by(Service.name).all()
