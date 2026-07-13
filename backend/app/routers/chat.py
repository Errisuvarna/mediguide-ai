import time
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.chat_history import ChatHistory
from app.models.analytics import AnalyticsEvent
from app.models.department import Department
from app.schemas.chat import ChatRequest, ChatResponse, SourceChunk
from app.rag.retriever import retrieve
from app.rag.prompt_builder import build_prompt, detect_emergency
from app.rag.gemini_client import generate_answer

router = APIRouter(prefix="/api", tags=["chat"])


def _match_department(message: str, db: Session) -> str | None:
    lowered = message.lower()
    departments = db.query(Department).all()
    for dept in departments:
        keywords = [k.strip().lower() for k in (dept.keywords or "").split(",") if k.strip()]
        haystack = [dept.name.lower(), *keywords]
        if any(term in lowered for term in haystack):
            return dept.name
    return None


@router.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest, db: Session = Depends(get_db)):
    start = time.perf_counter()

    is_emergency = detect_emergency(payload.message)
    retrieved = retrieve(payload.message)
    department = _match_department(payload.message, db)

    if is_emergency:
        reply_by_lang = {
            "en": "🚨 This sounds like it may be an EMERGENCY. Please go immediately to the "
                  "Emergency Department (ground floor, red signage) or alert any staff member now.",
            "hi": "🚨 यह एक आपातकालीन स्थिति लग रही है। कृपया तुरंत आपातकालीन विभाग (ग्राउंड फ्लोर, "
                  "लाल संकेत) जाएँ या अभी किसी स्टाफ सदस्य को सूचित करें।",
            "te": "🚨 ఇది అత్యవసర పరిస్థితిలా అనిపిస్తోంది. దయచేసి వెంటనే ఎమర్జెన్సీ విభాగానికి "
                  "(గ్రౌండ్ ఫ్లోర్, ఎరుపు గుర్తు) వెళ్లండి లేదా ఇప్పుడే సిబ్బందిని అప్రమత్తం చేయండి.",
        }
        reply = reply_by_lang.get(payload.language, reply_by_lang["en"])
    else:
        prompt = build_prompt(payload.message, payload.language, retrieved)
        reply = generate_answer(prompt, retrieved)

    elapsed_ms = (time.perf_counter() - start) * 1000

    db.add(ChatHistory(session_id=payload.session_id, role="user",
                        message=payload.message, language=payload.language))
    db.add(ChatHistory(session_id=payload.session_id, role="assistant",
                        message=reply, language=payload.language))
    db.add(AnalyticsEvent(
        event_type="voice_query" if payload.is_voice else "chat_query",
        department=department,
        language=payload.language,
        is_voice=1 if payload.is_voice else 0,
        is_emergency=1 if is_emergency else 0,
        response_time_ms=elapsed_ms,
        was_answered=1 if (retrieved or is_emergency) else 0,
    ))
    db.commit()

    return ChatResponse(
        session_id=payload.session_id,
        reply=reply,
        department_matched=department,
        is_emergency=is_emergency,
        sources=[
            SourceChunk(source_file=chunk.source_file, snippet=chunk.content[:180])
            for chunk, _score in retrieved
        ],
        response_time_ms=round(elapsed_ms, 1),
    )
