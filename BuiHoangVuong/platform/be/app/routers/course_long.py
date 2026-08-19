"""Course-long section: progress tracking, interventions, and analytics."""

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import case, func, select
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import CourseProgress, Intervention, RiskScore, Student
from ..schemas import AnalyticsSummary, InterventionCreate, InterventionRow, ProgressRow
from ..security import current_user

router = APIRouter(prefix="/api/course-long", tags=["course-long"], dependencies=[Depends(current_user)])


@router.get("/progress", response_model=list[ProgressRow])
def progress(db: Session = Depends(get_db)) -> list[ProgressRow]:
    """Per-student completion rate and study hours across the whole course."""
    totals = (
        select(
            Student.id,
            Student.name,
            Student.cohort,
            func.count(CourseProgress.id).label("weeks_tracked"),
            func.sum(CourseProgress.modules_completed).label("done"),
            func.sum(CourseProgress.modules_total).label("assigned"),
            func.sum(CourseProgress.hours_spent).label("hours"),
            func.max(CourseProgress.week_no).label("last_week"),
        )
        .join(CourseProgress, CourseProgress.student_id == Student.id)
        .group_by(Student.id)
        .order_by(Student.id)
    )
    rows = []
    for student_id, name, cohort, weeks, done, assigned, hours, last_week in db.execute(totals).all():
        last = db.execute(
            select(CourseProgress.modules_completed, CourseProgress.modules_total).where(
                CourseProgress.student_id == student_id, CourseProgress.week_no == last_week
            )
        ).first()
        rows.append(
            ProgressRow(
                student_id=student_id,
                name=name,
                cohort=cohort,
                weeks_tracked=weeks,
                completion_rate=round((done or 0) / (assigned or 1), 3),
                hours_spent=round(hours or 0, 1),
                last_week_completion=round((last[0] / last[1]) if last and last[1] else 0.0, 3),
            )
        )
    return rows


@router.get("/analytics/summary", response_model=AnalyticsSummary)
def analytics(db: Session = Depends(get_db)) -> AnalyticsSummary:
    """Cohort-level rollup shown on the Course-Long dashboard."""
    done, assigned, hours = db.execute(
        select(
            func.coalesce(func.sum(CourseProgress.modules_completed), 0),
            func.coalesce(func.sum(CourseProgress.modules_total), 0),
            func.coalesce(func.sum(CourseProgress.hours_spent), 0.0),
        )
    ).one()
    open_count, resolved_count = db.execute(
        select(
            func.count(case((Intervention.status == "open", 1))),
            func.count(case((Intervention.status == "resolved", 1))),
        )
    ).one()
    risk_mix = {
        category: count
        for category, count in db.execute(
            select(RiskScore.risk_category, func.count(RiskScore.id)).group_by(RiskScore.risk_category)
        ).all()
    }
    weekly = [
        {"week": float(week), "completion_rate": round((week_done or 0) / (week_assigned or 1), 3)}
        for week, week_done, week_assigned in db.execute(
            select(
                CourseProgress.week_no,
                func.sum(CourseProgress.modules_completed),
                func.sum(CourseProgress.modules_total),
            )
            .group_by(CourseProgress.week_no)
            .order_by(CourseProgress.week_no)
        ).all()
    ]
    return AnalyticsSummary(
        students=db.scalar(select(func.count(Student.id))) or 0,
        avg_completion_rate=round((done or 0) / (assigned or 1), 3),
        total_hours=round(hours or 0, 1),
        open_interventions=open_count or 0,
        resolved_interventions=resolved_count or 0,
        risk_mix=risk_mix,
        weekly_completion=weekly,
    )


@router.get("/interventions", response_model=list[InterventionRow])
def list_interventions(
    status_filter: str | None = Query(default=None, alias="status", pattern="^(open|resolved)$"),
    db: Session = Depends(get_db),
) -> list[InterventionRow]:
    """List support actions, newest first."""
    query = select(Intervention, Student.name).join(Student, Student.id == Intervention.student_id)
    if status_filter:
        query = query.where(Intervention.status == status_filter)
    query = query.order_by(Intervention.created_at.desc(), Intervention.id.desc())
    return [
        InterventionRow(student_name=name, **{c.name: getattr(item, c.name) for c in item.__table__.columns})
        for item, name in db.execute(query).all()
    ]


@router.post("/interventions", response_model=InterventionRow, status_code=status.HTTP_201_CREATED)
def create_intervention(payload: InterventionCreate, db: Session = Depends(get_db)) -> InterventionRow:
    """Open a new support action for a student."""
    student = db.get(Student, payload.student_id)
    if student is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Student {payload.student_id} not found")
    item = Intervention(**payload.model_dump(), status="open")
    db.add(item)
    db.commit()
    return InterventionRow(student_name=student.name, **{c.name: getattr(item, c.name) for c in item.__table__.columns})


@router.patch("/interventions/{intervention_id}", response_model=InterventionRow)
def resolve_intervention(intervention_id: int, db: Session = Depends(get_db)) -> InterventionRow:
    """Mark a support action resolved."""
    item = db.get(Intervention, intervention_id)
    if item is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Intervention {intervention_id} not found")
    item.status = "resolved"
    item.resolved_at = datetime.now(timezone.utc)
    db.commit()
    student = db.get(Student, item.student_id)
    return InterventionRow(
        student_name=student.name if student else "", **{c.name: getattr(item, c.name) for c in item.__table__.columns}
    )
