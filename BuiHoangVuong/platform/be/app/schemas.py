"""Pydantic request/response contracts."""

from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: Literal["bearer"] = "bearer"
    username: str


class RankingRow(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    student_id: int
    external_id: str
    name: str
    avg_score: float
    score_trend: float
    failed_count: int
    logins_7d: int
    risk_score: int
    risk_category: str
    explanation: str
    computed_at: datetime


class JobResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    status: str
    students_scored: int
    error: Optional[str] = None
    requested_at: datetime
    finished_at: Optional[datetime] = None


class SyncResponse(BaseModel):
    students: int
    high: int
    mid: int
    low: int


class ProgressRow(BaseModel):
    student_id: int
    name: str
    cohort: str
    weeks_tracked: int
    completion_rate: float = Field(description="Modules completed / modules assigned, 0-1")
    hours_spent: float
    last_week_completion: float


class AnalyticsSummary(BaseModel):
    students: int
    avg_completion_rate: float
    total_hours: float
    open_interventions: int
    resolved_interventions: int
    risk_mix: dict[str, int]
    weekly_completion: list[dict[str, float]]


class InterventionCreate(BaseModel):
    student_id: int
    kind: str = Field(examples=["tutoring", "mentor call", "parent contact"])
    owner: str
    note: str = ""


class InterventionRow(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    student_id: int
    student_name: str
    kind: str
    status: str
    owner: str
    note: str
    created_at: datetime
    resolved_at: Optional[datetime] = None
