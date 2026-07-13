from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.doctor import Doctor
from app.schemas.doctor import DoctorOut

router = APIRouter(prefix="/api/doctors", tags=["doctors"])


@router.get("", response_model=List[DoctorOut])
def list_doctors(
    department_id: Optional[int] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
):
    query = db.query(Doctor)
    if department_id:
        query = query.filter(Doctor.department_id == department_id)
    if search:
        query = query.filter(Doctor.full_name.ilike(f"%{search}%"))
    return query.order_by(Doctor.full_name).all()
