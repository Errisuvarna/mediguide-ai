from typing import List, Dict
from pydantic import BaseModel


class DashboardSummary(BaseModel):
    total_queries: int
    today_queries: int
    weekly_queries: int
    monthly_queries: int
    emergency_queries: int
    avg_response_time_ms: float
    feedback_score: float
    patient_satisfaction_pct: float


class ChartPoint(BaseModel):
    label: str
    value: float


class DashboardCharts(BaseModel):
    department_wise_queries: List[ChartPoint]
    daily_trend: List[ChartPoint]
    weekly_trend: List[ChartPoint]
    monthly_trend: List[ChartPoint]
    most_asked_questions: List[ChartPoint]
    popular_services: List[ChartPoint]
    voice_usage: List[ChartPoint]
    language_usage: List[ChartPoint]
    unanswered_questions: List[ChartPoint]


class RecentQuery(BaseModel):
    message: str
    department: str | None
    language: str
    created_at: str
