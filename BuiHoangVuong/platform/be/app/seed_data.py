"""Deterministic demo data for both sections, ported from the prototype's sync.py profiles."""

from datetime import datetime, timedelta, timezone
import random
from typing import Dict, List, Tuple

from sqlalchemy import delete, func, select
from sqlalchemy.orm import Session

from .models import Assessment, CourseProgress, Intervention, Login, RiskScore, ScoringJob, Student

# profile -> (count, base score range, per-assessment trend range, logins in last 7 days)
PROFILES: Dict[str, Tuple[int, Tuple[float, float], Tuple[float, float], Tuple[int, int]]] = {
    "high": (10, (4.8, 5.6), (-0.80, -0.60), (0, 2)),
    "mid": (15, (6.2, 7.2), (-0.45, -0.30), (3, 4)),
    "low": (25, (7.8, 9.5), (0.00, 0.25), (8, 20)),
}
COURSE_WEEKS = 8
SEED = 2026


def seed_in_class(session: Session, seed: int = SEED) -> Dict[str, int]:
    """Rebuild students plus their in-class signals. Returns the profile mix."""
    random.seed(seed)
    now = datetime.now(timezone.utc)
    for model in (RiskScore, ScoringJob, Intervention, CourseProgress, Login, Assessment, Student):
        session.execute(delete(model))
    session.commit()

    roster: List[str] = [name for name, cfg in PROFILES.items() for _ in range(cfg[0])]
    random.shuffle(roster)
    for index, profile in enumerate(roster, start=1):
        _, base_range, trend_range, recent_range = PROFILES[profile]
        student = Student(
            external_id=f"HS{index:03d}",
            name=f"Học sinh {index:02d}",
            email=f"hs{index:02d}@truong.edu.vn",
            cohort="2026A" if index % 2 else "2026B",
        )
        session.add(student)
        session.flush()

        base = random.uniform(*base_range)
        trend = random.uniform(*trend_range)
        for assessment_no in range(4):
            score = max(0.0, min(10.0, base + trend * assessment_no + random.uniform(-0.3, 0.3)))
            session.add(
                Assessment(student_id=student.id, assessment_no=assessment_no + 1, score=round(score, 2))
            )
        recent = random.randint(*recent_range)
        older = random.randint(3, 12)
        for days_ago in [random.uniform(0, 5.5) for _ in range(recent)] + [random.uniform(8, 45) for _ in range(older)]:
            session.add(Login(student_id=student.id, login_time=now - timedelta(days=days_ago)))

        _seed_course_long(session, student, profile, now)
    session.commit()
    return {"students": len(roster), **{profile: cfg[0] for profile, cfg in PROFILES.items()}}


def _seed_course_long(session: Session, student: Student, profile: str, now: datetime) -> None:
    """Attach weekly progress and, for weaker profiles, an open intervention."""
    completion = {"high": (0.25, 0.55), "mid": (0.55, 0.8), "low": (0.8, 1.0)}[profile]
    modules_total = 5
    for week_no in range(1, COURSE_WEEKS + 1):
        rate = min(1.0, max(0.0, random.uniform(*completion) + random.uniform(-0.08, 0.08)))
        session.add(
            CourseProgress(
                student_id=student.id,
                week_no=week_no,
                modules_completed=round(rate * modules_total),
                modules_total=modules_total,
                hours_spent=round(rate * random.uniform(3.0, 6.5), 1),
                updated_at=now - timedelta(days=(COURSE_WEEKS - week_no) * 7),
            )
        )
    if profile == "high":
        session.add(
            Intervention(
                student_id=student.id,
                kind="tutoring",
                status="open",
                owner="teacher",
                note="Mở tự động từ dữ liệu đồng bộ: tiến độ và điểm đều thấp.",
                created_at=now - timedelta(days=random.randint(1, 10)),
            )
        )
    elif profile == "mid" and random.random() < 0.4:
        session.add(
            Intervention(
                student_id=student.id,
                kind="mentor call",
                status="resolved",
                owner="admin",
                note="Đã gọi nhắc nhở, học sinh cam kết hoàn thành bài còn thiếu.",
                created_at=now - timedelta(days=random.randint(11, 25)),
                resolved_at=now - timedelta(days=random.randint(1, 9)),
            )
        )


def seed_if_empty(session: Session) -> bool:
    """Seed on first boot only. Returns True when data was written."""
    if session.scalar(select(func.count(Student.id))):
        return False
    seed_in_class(session)
    return True
