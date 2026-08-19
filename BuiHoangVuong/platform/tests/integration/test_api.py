"""Integration tests driving the FastAPI app through TestClient."""

import pytest


def test_health_reports_database(api_client):
    response = api_client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "database": "reachable"}


def test_login_rejects_bad_password(api_client):
    response = api_client.post("/api/auth/login", json={"username": "teacher", "password": "nope"})
    assert response.status_code == 401


def test_protected_routes_require_a_token(api_client):
    assert api_client.get("/api/in-class/ranking").status_code == 401
    assert api_client.get("/api/course-long/progress").status_code == 401


def test_me_returns_username(api_client, auth_headers):
    assert api_client.get("/api/auth/me", headers=auth_headers).json() == {"username": "teacher"}


def test_sync_then_score_then_rank(api_client, auth_headers, monkeypatch):
    from app import scoring_service
    from app.db import SessionLocal
    from app.models import ScoringJob

    # Run the Celery task inline so the flow is testable without a broker.
    def run_now(job_id):
        session = SessionLocal()
        job = session.get(ScoringJob, job_id)
        job.status = "done"
        job.students_scored = scoring_service.score_all(session, job_id=job_id)
        session.commit()
        session.close()
        return type("Task", (), {"id": f"inline-{job_id}"})()

    monkeypatch.setattr("app.routers.in_class.score_all_students.delay", run_now)

    mix = api_client.post("/api/in-class/sync", headers=auth_headers).json()
    assert mix["students"] == 50 and mix["high"] == 10

    job = api_client.post("/api/in-class/score", headers=auth_headers)
    assert job.status_code == 202
    assert api_client.get(f"/api/in-class/jobs/{job.json()['id']}", headers=auth_headers).json()["status"] == "done"

    ranking = api_client.get("/api/in-class/ranking", headers=auth_headers).json()
    assert len(ranking) == 50
    assert ranking[0]["risk_score"] >= ranking[-1]["risk_score"]
    assert ranking[0]["explanation"].startswith("Xếp hạng #1")

    high_only = api_client.get("/api/in-class/ranking?category=High%20Risk", headers=auth_headers).json()
    assert high_only and all(row["risk_category"] == "High Risk" for row in high_only)


def test_score_without_students_returns_409(api_client, auth_headers):
    assert api_client.post("/api/in-class/score", headers=auth_headers).status_code == 409


def test_course_long_analytics_and_interventions(api_client, auth_headers):
    api_client.post("/api/in-class/sync", headers=auth_headers)

    summary = api_client.get("/api/course-long/analytics/summary", headers=auth_headers).json()
    assert summary["students"] == 50
    assert 0 <= summary["avg_completion_rate"] <= 1
    assert len(summary["weekly_completion"]) == 8

    progress = api_client.get("/api/course-long/progress", headers=auth_headers).json()
    assert len(progress) == 50 and progress[0]["weeks_tracked"] == 8

    created = api_client.post(
        "/api/course-long/interventions",
        headers=auth_headers,
        json={"student_id": 1, "kind": "tutoring", "owner": "teacher", "note": "test"},
    )
    assert created.status_code == 201 and created.json()["status"] == "open"

    resolved = api_client.patch(f"/api/course-long/interventions/{created.json()['id']}", headers=auth_headers)
    assert resolved.status_code == 200 and resolved.json()["status"] == "resolved"

    assert not any(
        item["id"] == created.json()["id"]
        for item in api_client.get("/api/course-long/interventions?status=open", headers=auth_headers).json()
    )


@pytest.mark.parametrize("path", ["/api/course-long/interventions/9999", "/api/in-class/jobs/9999"])
def test_missing_resources_return_404(api_client, auth_headers, path):
    method = api_client.patch if "interventions" in path else api_client.get
    assert method(path, headers=auth_headers).status_code == 404
