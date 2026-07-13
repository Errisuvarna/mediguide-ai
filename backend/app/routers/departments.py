from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.department import Department
from app.schemas.department import DepartmentOut

router = APIRouter(prefix="/api/departments", tags=["departments"])


@router.get("", response_model=List[DepartmentOut])
def list_departments(search: Optional[str] = Query(None), db: Session = Depends(get_db)):
    query = db.query(Department)
    if search:
        like = f"%{search.lower()}%"
        query = query.filter(
            (Department.name.ilike(like))
            | (Department.description.ilike(like))
            | (Department.keywords.ilike(like))
        )
    return query.order_by(Department.name).all()


@router.get("/{department_id}", response_model=DepartmentOut)
def get_department(department_id: int, db: Session = Depends(get_db)):
    dept = db.query(Department).get(department_id)
    if not dept:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Department not found")
    return dept
