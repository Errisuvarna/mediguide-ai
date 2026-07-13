"""
Loads the generated dataset/*.json files into the database.
Idempotent: skips seeding if departments already exist.

Run standalone:
    python -m app.seed.seed_db
(also runs automatically the first time you start the API, see app/main.py)
"""
import json
import logging
from pathlib import Path

from app.database import SessionLocal, init_db
from app.models.department import Department
from app.models.doctor import Doctor
from app.models.service import Service
from app.models.procedure import Procedure
from app.models.document import RequiredDocument
from app.models.building import Building
from app.models.floor import Floor
from app.models.room import Room
from app.models.faq import FAQ
from app.models.hospital_map import HospitalMapPoint

logger = logging.getLogger(__name__)
DATASET_DIR = Path(__file__).resolve().parents[3] / "dataset"


def _load(name: str):
    path = DATASET_DIR / f"{name}.json"
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))


def seed() -> None:
    init_db()
    db = SessionLocal()
    try:
        if db.query(Department).count() > 0:
            logger.info("Database already seeded, skipping.")
            return

        for row in _load("departments"):
            db.add(Department(**row))
        db.commit()

        for row in _load("doctors"):
            db.add(Doctor(**row))
        db.commit()

        for row in _load("services"):
            db.add(Service(**row))
        db.commit()

        for row in _load("procedures"):
            db.add(Procedure(**row))
        db.commit()

        for row in _load("required_documents"):
            db.add(RequiredDocument(**row))
        db.commit()

        for row in _load("buildings"):
            db.add(Building(**row))
        db.commit()

        for row in _load("floors"):
            db.add(Floor(**row))
        db.commit()

        for row in _load("rooms"):
            db.add(Room(**row))
        db.commit()

        for row in _load("faqs"):
            db.add(FAQ(**row))
        db.commit()

        for row in _load("hospital_map_points"):
            db.add(HospitalMapPoint(**row))
        db.commit()

        logger.info("Database seeded successfully.")
    finally:
        db.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    seed()
