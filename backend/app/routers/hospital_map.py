from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.hospital_map import HospitalMapPoint
from app.schemas.hospital_map import HospitalMapPointOut

router = APIRouter(prefix="/api/hospital-map", tags=["hospital-map"])


@router.get("", response_model=List[HospitalMapPointOut])
def get_map_points(db: Session = Depends(get_db)):
    return db.query(HospitalMapPoint).order_by(HospitalMapPoint.building_name).all()
