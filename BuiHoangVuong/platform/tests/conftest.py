"""Fixtures shared by unit and integration tests."""

import os
import sys
import tempfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "be"))
sys.path.insert(0, str(ROOT / "shared"))

# A file-backed SQLite database keeps the API importable without Postgres; every
# connection in Starlette's threadpool then sees the same data. Integration tests
# can be pointed at Postgres instead by exporting DATABASE_URL before pytest runs.
_TEST_DB = Path(tempfile.gettempdir()) / "ews_pytest.db"
_TEST_DB.unlink(missing_ok=True)
os.environ.setdefault("DATABASE_URL", f"sqlite+pysqlite:///{_TEST_DB}")
os.environ.setdefault("AUTH_SECRET", "test-secret")
os.environ.setdefault("SEED_ON_START", "false")


@pytest.fixture(scope="session")
def features_high():
    """Worst-case signals: every rule fires."""
    return {"avg_score": 4.2, "score_trend": -0.75, "failed_count": 3, "logins_7d": 1}


@pytest.fixture(scope="session")
def features_low():
    """Healthy signals: no rule fires."""
    return {"avg_score": 8.6, "score_trend": 0.12, "failed_count": 0, "logins_7d": 12}


@pytest.fixture
def api_client():
    """FastAPI TestClient bound to a throwaway SQLite database."""
    from fastapi.testclient import TestClient

    from app.db import engine
    from app.main import app
    from app.models import Base

    Base.metadata.create_all(engine)
    with TestClient(app) as client:
        yield client
    Base.metadata.drop_all(engine)


@pytest.fixture
def auth_headers(api_client):
    """Bearer header for the demo teacher account."""
    response = api_client.post("/api/auth/login", json={"username": "teacher", "password": "teacher123"})
    assert response.status_code == 200, response.text
    return {"Authorization": f"Bearer {response.json()['access_token']}"}
