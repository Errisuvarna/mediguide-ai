"""
Import every model module so Base.metadata is fully populated
before init_db() runs create_all().
"""
from app.models.user import User
from app.models.department import Department
from app.models.doctor import Doctor, DoctorSpecialization
from app.models.building import Building
from app.models.floor import Floor
from app.models.room import Room
from app.models.service import Service
from app.models.procedure import Procedure
from app.models.document import RequiredDocument
from app.models.hospital_map import HospitalMapPoint
from app.models.appointment import Appointment
from app.models.faq import FAQ
from app.models.feedback import Feedback
from app.models.analytics import AnalyticsEvent
from app.models.chat_history import ChatHistory
from app.models.knowledge_document import KnowledgeDocument

__all__ = [
    "User", "Department", "Doctor", "DoctorSpecialization", "Building",
    "Floor", "Room", "Service", "Procedure", "RequiredDocument",
    "HospitalMapPoint", "Appointment", "FAQ", "Feedback", "AnalyticsEvent",
    "ChatHistory", "KnowledgeDocument",
]
