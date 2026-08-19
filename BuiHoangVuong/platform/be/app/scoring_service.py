"""Bridge between the ORM and the shared rule engine."""

from datetime import datetime, timedelta, timezone
from typing import Optional

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from ews_shared import build_features, calculate_risk_score, categorize, explain

from .models import Assessment, Login, RiskScore, Student


def score_student(session: Session, student: Student, rank: int, job_id: Optional[int] = None) -> RiskScore:
    """Compute one student's features, score, band, and explanation."""
    scores = list(
        session.scalars(
            select(Assessment.score).where(Assessment.student_id == student.id).order_by(Assessment.assessment_no)
        )
    )
    cutoff = datetime.now(timezone.utc) - timedelta(days=7)
    logins_7d = session.scalar(
        select(func.count(Login.id)).where(Login.student_id == student.id, Login.login_time >= cutoff)
    )
    features = build_features(scores, logins_7d or 0)
    risk = calculate_risk_score(features)
    category = categorize(risk)
    row = {**features, "risk_score": risk, "risk_category": category}
    return RiskScore(
        student_id=student.id,
        job_id=job_id,
        risk_score=risk,
        risk_category=category,
        explanation=explain(row, rank) if rank else "",
        **features,
    )


def score_all(session: Session, job_id: Optional[int] = None) -> int:
    """Re-score every student, replacing the previous snapshot. Returns the row count."""
    students = list(session.scalars(select(Student).order_by(Student.id)))
    if not students:
        return 0
    session.query(RiskScore).delete()
    unranked = [score_student(session, student, rank=0, job_id=job_id) for student in students]
    unranked.sort(key=lambda row: row.risk_score, reverse=True)
    for rank, row in enumerate(unranked, start=1):
        row.explanation = explain(
            {
                "avg_score": row.avg_score,
                "score_trend": row.score_trend,
                "failed_count": row.failed_count,
                "logins_7d": row.logins_7d,
                "risk_score": row.risk_score,
                "risk_category": row.risk_category,
            },
            rank,
        )
        session.add(row)
    session.commit()
    return len(unranked)
