"""Initial schema: students, in-class signals, scoring output, course-long tracking.

Revision ID: 0001
Revises:
"""

from alembic import op
import sqlalchemy as sa

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "students",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("external_id", sa.String(32), nullable=False, unique=True),
        sa.Column("name", sa.String(120), nullable=False),
        sa.Column("email", sa.String(160), nullable=False),
        sa.Column("cohort", sa.String(40), nullable=False, server_default="2026A"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_students_external_id", "students", ["external_id"])

    op.create_table(
        "assessments",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("student_id", sa.Integer, sa.ForeignKey("students.id", ondelete="CASCADE"), nullable=False),
        sa.Column("assessment_no", sa.Integer, nullable=False),
        sa.Column("score", sa.Float, nullable=False),
        sa.Column("taken_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_assessments_student_id", "assessments", ["student_id"])

    op.create_table(
        "logins",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("student_id", sa.Integer, sa.ForeignKey("students.id", ondelete="CASCADE"), nullable=False),
        sa.Column("login_time", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_logins_student_id", "logins", ["student_id"])
    op.create_index("ix_logins_login_time", "logins", ["login_time"])

    op.create_table(
        "scoring_jobs",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("task_id", sa.String(64)),
        sa.Column("status", sa.String(20), nullable=False, server_default="queued"),
        sa.Column("students_scored", sa.Integer, nullable=False, server_default="0"),
        sa.Column("error", sa.Text),
        sa.Column("requested_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("finished_at", sa.DateTime(timezone=True)),
    )
    op.create_index("ix_scoring_jobs_status", "scoring_jobs", ["status"])
    op.create_index("ix_scoring_jobs_task_id", "scoring_jobs", ["task_id"])

    op.create_table(
        "risk_scores",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("student_id", sa.Integer, sa.ForeignKey("students.id", ondelete="CASCADE"), nullable=False),
        sa.Column("job_id", sa.Integer, sa.ForeignKey("scoring_jobs.id", ondelete="SET NULL")),
        sa.Column("avg_score", sa.Float, nullable=False),
        sa.Column("score_trend", sa.Float, nullable=False),
        sa.Column("failed_count", sa.Integer, nullable=False),
        sa.Column("logins_7d", sa.Integer, nullable=False),
        sa.Column("risk_score", sa.Integer, nullable=False),
        sa.Column("risk_category", sa.String(20), nullable=False),
        sa.Column("explanation", sa.Text, nullable=False),
        sa.Column("computed_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_risk_scores_student_id", "risk_scores", ["student_id"])
    op.create_index("ix_risk_scores_risk_score", "risk_scores", ["risk_score"])
    op.create_index("ix_risk_scores_risk_category", "risk_scores", ["risk_category"])

    op.create_table(
        "course_progress",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("student_id", sa.Integer, sa.ForeignKey("students.id", ondelete="CASCADE"), nullable=False),
        sa.Column("week_no", sa.Integer, nullable=False),
        sa.Column("modules_completed", sa.Integer, nullable=False),
        sa.Column("modules_total", sa.Integer, nullable=False),
        sa.Column("hours_spent", sa.Float, nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_course_progress_student_id", "course_progress", ["student_id"])
    op.create_index("ix_course_progress_week_no", "course_progress", ["week_no"])

    op.create_table(
        "interventions",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("student_id", sa.Integer, sa.ForeignKey("students.id", ondelete="CASCADE"), nullable=False),
        sa.Column("kind", sa.String(40), nullable=False),
        sa.Column("status", sa.String(20), nullable=False, server_default="open"),
        sa.Column("owner", sa.String(60), nullable=False),
        sa.Column("note", sa.Text, nullable=False, server_default=""),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("resolved_at", sa.DateTime(timezone=True)),
    )
    op.create_index("ix_interventions_student_id", "interventions", ["student_id"])
    op.create_index("ix_interventions_status", "interventions", ["status"])


def downgrade() -> None:
    for table in (
        "interventions",
        "course_progress",
        "risk_scores",
        "scoring_jobs",
        "logins",
        "assessments",
        "students",
    ):
        op.drop_table(table)
