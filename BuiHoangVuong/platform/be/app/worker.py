"""Celery worker: async scoring jobs off the Redis queue."""

from datetime import datetime, timezone

from celery import Celery

from .config import REDIS_URL
from .db import SessionLocal
from .models import ScoringJob
from .scoring_service import score_all

celery_app = Celery("ews", broker=REDIS_URL, backend=REDIS_URL)
celery_app.conf.update(task_track_started=True, task_time_limit=300, worker_hijack_root_logger=False)


@celery_app.task(name="ews.score_all_students")
def score_all_students(job_id: int) -> dict[str, int | str]:
    """Score every student and mark the job record done or failed."""
    session = SessionLocal()
    job = session.get(ScoringJob, job_id)
    try:
        if job is None:
            raise ValueError(f"Scoring job {job_id} not found")
        job.status = "running"
        session.commit()
        scored = score_all(session, job_id=job_id)
        job.status = "done"
        job.students_scored = scored
        job.finished_at = datetime.now(timezone.utc)
        session.commit()
        return {"job_id": job_id, "students_scored": scored, "status": "done"}
    except Exception as error:  # noqa: BLE001 - recorded on the job row for the UI
        session.rollback()
        if job is not None:
            job.status = "failed"
            job.error = str(error)
            job.finished_at = datetime.now(timezone.utc)
            session.commit()
        raise
    finally:
        session.close()
