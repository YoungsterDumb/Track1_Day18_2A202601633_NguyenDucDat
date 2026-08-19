"""Shared ORM models: in-class signals, course-long tracking, and scoring jobs."""

from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True)
    external_id: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(120))
    email: Mapped[str] = mapped_column(String(160))
    cohort: Mapped[str] = mapped_column(String(40), default="2026A")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    assessments: Mapped[list["Assessment"]] = relationship(back_populates="student", cascade="all, delete-orphan")
    logins: Mapped[list["Login"]] = relationship(back_populates="student", cascade="all, delete-orphan")
    risk_scores: Mapped[list["RiskScore"]] = relationship(back_populates="student", cascade="all, delete-orphan")
    progress: Mapped[list["CourseProgress"]] = relationship(back_populates="student", cascade="all, delete-orphan")
    interventions: Mapped[list["Intervention"]] = relationship(back_populates="student", cascade="all, delete-orphan")


class Assessment(Base):
    """In-class signal: one graded assessment (0-10)."""

    __tablename__ = "assessments"

    id: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id", ondelete="CASCADE"), index=True)
    assessment_no: Mapped[int] = mapped_column(Integer)
    score: Mapped[float] = mapped_column(Float)
    taken_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    student: Mapped[Student] = relationship(back_populates="assessments")


class Login(Base):
    """In-class signal: one LMS login event."""

    __tablename__ = "logins"

    id: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id", ondelete="CASCADE"), index=True)
    login_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)

    student: Mapped[Student] = relationship(back_populates="logins")


class RiskScore(Base):
    """Output of a scoring job: features, score, band, and the Vietnamese explanation."""

    __tablename__ = "risk_scores"

    id: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id", ondelete="CASCADE"), index=True)
    job_id: Mapped[int | None] = mapped_column(ForeignKey("scoring_jobs.id", ondelete="SET NULL"), nullable=True)
    avg_score: Mapped[float] = mapped_column(Float)
    score_trend: Mapped[float] = mapped_column(Float)
    failed_count: Mapped[int] = mapped_column(Integer)
    logins_7d: Mapped[int] = mapped_column(Integer)
    risk_score: Mapped[int] = mapped_column(Integer, index=True)
    risk_category: Mapped[str] = mapped_column(String(20), index=True)
    explanation: Mapped[str] = mapped_column(Text)
    computed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    student: Mapped[Student] = relationship(back_populates="risk_scores")


class ScoringJob(Base):
    """Async job record written by the API and updated by the Celery worker."""

    __tablename__ = "scoring_jobs"

    id: Mapped[int] = mapped_column(primary_key=True)
    task_id: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    status: Mapped[str] = mapped_column(String(20), default="queued", index=True)
    students_scored: Mapped[int] = mapped_column(Integer, default=0)
    error: Mapped[str | None] = mapped_column(Text, nullable=True)
    requested_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class CourseProgress(Base):
    """Course-long signal: weekly module completion and study hours."""

    __tablename__ = "course_progress"

    id: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id", ondelete="CASCADE"), index=True)
    week_no: Mapped[int] = mapped_column(Integer, index=True)
    modules_completed: Mapped[int] = mapped_column(Integer)
    modules_total: Mapped[int] = mapped_column(Integer)
    hours_spent: Mapped[float] = mapped_column(Float)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    student: Mapped[Student] = relationship(back_populates="progress")


class Intervention(Base):
    """Course-long action: a support step opened for a student and tracked to closure."""

    __tablename__ = "interventions"

    id: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id", ondelete="CASCADE"), index=True)
    kind: Mapped[str] = mapped_column(String(40))
    status: Mapped[str] = mapped_column(String(20), default="open", index=True)
    owner: Mapped[str] = mapped_column(String(60))
    note: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    student: Mapped[Student] = relationship(back_populates="interventions")
