from collections import Counter
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models.analytics import AnalyticsEvent
from app.models.chat_history import ChatHistory
from app.models.feedback import Feedback
from app.schemas.analytics import DashboardSummary, DashboardCharts, ChartPoint, RecentQuery

router = APIRouter(prefix="/api/analytics", tags=["analytics"])


@router.get("", response_model=dict)
def get_analytics(db: Session = Depends(get_db)):
    now = datetime.now(timezone.utc)
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    week_start = now - timedelta(days=7)
    month_start = now - timedelta(days=30)

    events = db.query(AnalyticsEvent).all()
    total_queries = len(events)
    today_queries = sum(1 for e in events if e.created_at >= today_start)
    weekly_queries = sum(1 for e in events if e.created_at >= week_start)
    monthly_queries = sum(1 for e in events if e.created_at >= month_start)
    emergency_queries = sum(1 for e in events if e.is_emergency)
    avg_response_time = (
        sum(e.response_time_ms for e in events) / total_queries if total_queries else 0.0
    )

    feedback_rows = db.query(Feedback).all()
    feedback_score = (
        sum(f.rating for f in feedback_rows) / len(feedback_rows) if feedback_rows else 0.0
    )
    satisfaction_pct = (feedback_score / 5.0) * 100 if feedback_rows else 0.0

    summary = DashboardSummary(
        total_queries=total_queries,
        today_queries=today_queries,
        weekly_queries=weekly_queries,
        monthly_queries=monthly_queries,
        emergency_queries=emergency_queries,
        avg_response_time_ms=round(avg_response_time, 1),
        feedback_score=round(feedback_score, 2),
        patient_satisfaction_pct=round(satisfaction_pct, 1),
    )

    dept_counts = Counter(e.department for e in events if e.department)
    lang_counts = Counter(e.language for e in events)
    voice_counts = Counter("Voice" if e.is_voice else "Text" for e in events)
    unanswered = Counter(
        e.department or "Unclassified" for e in events if not e.was_answered
    )

    day_labels = [(now - timedelta(days=i)).strftime("%a") for i in range(6, -1, -1)]
    day_buckets = Counter()
    for e in events:
        delta_days = (now.date() - e.created_at.date()).days
        if 0 <= delta_days <= 6:
            day_buckets[(now - timedelta(days=delta_days)).strftime("%a")] += 1
    daily_trend = [ChartPoint(label=d, value=day_buckets.get(d, 0)) for d in day_labels]

    week_labels = [f"Week {i+1}" for i in range(4)]
    week_buckets = Counter()
    for e in events:
        delta_days = (now.date() - e.created_at.date()).days
        if 0 <= delta_days <= 27:
            week_buckets[f"Week {4 - (delta_days // 7)}"] += 1
    weekly_trend = [ChartPoint(label=w, value=week_buckets.get(w, 0)) for w in week_labels]

    month_labels = [(now - timedelta(days=30 * i)).strftime("%b") for i in range(5, -1, -1)]
    month_buckets = Counter()
    for e in events:
        month_buckets[e.created_at.strftime("%b")] += 1
    monthly_trend = [ChartPoint(label=m, value=month_buckets.get(m, 0)) for m in month_labels]

    question_counts = Counter(
        (m.message[:60] for m in db.query(ChatHistory).filter(ChatHistory.role == "user").all())
    )
    most_asked = [ChartPoint(label=q, value=c) for q, c in question_counts.most_common(8)]

    charts = DashboardCharts(
        department_wise_queries=[ChartPoint(label=k, value=v) for k, v in dept_counts.most_common(10)],
        daily_trend=daily_trend,
        weekly_trend=weekly_trend,
        monthly_trend=monthly_trend,
        most_asked_questions=most_asked,
        popular_services=[ChartPoint(label=k, value=v) for k, v in dept_counts.most_common(6)],
        voice_usage=[ChartPoint(label=k, value=v) for k, v in voice_counts.items()],
        language_usage=[ChartPoint(label=k.upper(), value=v) for k, v in lang_counts.items()],
        unanswered_questions=[ChartPoint(label=k, value=v) for k, v in unanswered.most_common(6)],
    )

    recent = (
        db.query(AnalyticsEvent)
        .order_by(AnalyticsEvent.created_at.desc())
        .limit(10)
        .all()
    )
    recent_queries = [
        RecentQuery(
            message=f"{e.event_type} query",
            department=e.department,
            language=e.language,
            created_at=e.created_at.isoformat(),
        )
        for e in recent
    ]

    return {
        "summary": summary.model_dump(),
        "charts": charts.model_dump(),
        "recent_queries": [r.model_dump() for r in recent_queries],
    }
