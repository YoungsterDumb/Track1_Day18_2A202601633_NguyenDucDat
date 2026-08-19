"""In-class section: sync signals, enqueue scoring jobs, read the ranking."""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import RiskScore, ScoringJob, Student
from ..schemas import JobResponse, RankingRow, SyncResponse
from ..security import current_user
from ..seed_data import seed_in_class
from ..worker import score_all_students

router = APIRouter(prefix="/api/in-class", tags=["in-class"], dependencies=[Depends(current_user)])


@router.post("/sync", response_model=SyncResponse)
def sync(db: Session = Depends(get_db)) -> SyncResponse:
    """Mock a school-system pull: rebuild students, assessments, and logins."""
    mix = seed_in_class(db)
    return SyncResponse(**mix)


@router.post("/score", response_model=JobResponse, status_code=status.HTTP_202_ACCEPTED)
def enqueue_scoring(db: Session = Depends(get_db)) -> ScoringJob:
    """Queue an async scoring run and return the job to poll."""
    if not db.scalar(select(Student.id).limit(1)):
        raise HTTPException(status.HTTP_409_CONFLICT, "No students yet — run /api/in-class/sync first.")
    job = ScoringJob(status="queued")
    db.add(job)
    db.commit()
    task = score_all_students.delay(job.id)
    job.task_id = task.id
    db.commit()
    return job


@router.get("/jobs/{job_id}", response_model=JobResponse)
def get_job(job_id: int, db: Session = Depends(get_db)) -> ScoringJob:
    """Poll one scoring job."""
    job = db.get(ScoringJob, job_id)
    if job is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Job {job_id} not found")
    return job


@router.get("/ranking", response_model=list[RankingRow])
def ranking(
    category: str | None = Query(default=None, pattern="^(High|Medium|Low) Risk$"),
    limit: int = Query(default=100, ge=1, le=500),
    db: Session = Depends(get_db),
) -> list[RankingRow]:
    """Return the latest ranking, highest risk first."""
    query = select(RiskScore, Student).join(Student, Student.id == RiskScore.student_id)
    if category:
        query = query.where(RiskScore.risk_category == category)
    query = query.order_by(RiskScore.risk_score.desc(), Student.id).limit(limit)
    return [
        RankingRow(
            student_id=student.id,
            external_id=student.external_id,
            name=student.name,
            avg_score=score.avg_score,
            score_trend=score.score_trend,
            failed_count=score.failed_count,
            logins_7d=score.logins_7d,
            risk_score=score.risk_score,
            risk_category=score.risk_category,
            explanation=score.explanation,
            computed_at=score.computed_at,
        )
        for score, student in db.execute(query).all()
    ]


@router.get("/students/{student_id}/explanation")
def explanation(student_id: int, db: Session = Depends(get_db)) -> dict[str, object]:
    """Return the Vietnamese 'why this rank?' text for one student."""
    score = db.scalar(
        select(RiskScore).where(RiskScore.student_id == student_id).order_by(RiskScore.computed_at.desc()).limit(1)
    )
    if score is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"No score for student {student_id}")
    return {
        "student_id": student_id,
        "risk_score": score.risk_score,
        "risk_category": score.risk_category,
        "explanation": score.explanation,
    }
