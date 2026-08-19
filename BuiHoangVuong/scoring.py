"""Feature engineering and rule-based student risk scoring."""

from datetime import datetime, timedelta
import sqlite3
from pathlib import Path
from typing import Dict, Union

import pandas as pd

DbPath = Union[str, Path]


def calculate_features(db_path: DbPath, student_id: int) -> Dict[str, float]:
    """Return score, trend, failed-assessment, and recent-login features."""
    cutoff = (datetime.now() - timedelta(days=7)).isoformat(timespec="seconds")
    with sqlite3.connect(db_path) as connection:
        assessments = connection.execute(
            "SELECT score FROM assessments WHERE student_id = ? ORDER BY assessment_no",
            (student_id,),
        ).fetchall()
        if not assessments:
            raise ValueError(f"No assessment data found for student {student_id}.")
        average = sum(row[0] for row in assessments) / len(assessments)
        trend = (assessments[-1][0] - assessments[0][0]) / max(len(assessments) - 1, 1)
        failed = sum(row[0] < 5 for row in assessments)
        logins = connection.execute(
            "SELECT COUNT(*) FROM logins WHERE student_id = ? AND login_time >= ?",
            (student_id, cutoff),
        ).fetchone()[0]
    return {
        "avg_score": round(average, 2),
        "score_trend": round(trend, 2),
        "failed_count": int(failed),
        "logins_7d": int(logins),
    }


def calculate_risk_score(features: Dict[str, float]) -> int:
    """Calculate a capped 0-100 risk score from the supplied features."""
    score = 0
    average = features["avg_score"]
    trend = features["score_trend"]
    failed = features["failed_count"]
    logins = features["logins_7d"]
    score += 20 if average < 5 else 10 if average < 7 else 0
    score += 25 if trend < -0.15 else 12 if trend < -0.05 else 0
    score += 15 if failed >= 2 else 7 if failed == 1 else 0
    score += 15 if logins < 3 else 7 if logins < 5 else 0
    return min(100, score)


def get_ranking(db_path: DbPath) -> pd.DataFrame:
    """Return all students ranked from highest to lowest risk."""
    columns = ["student_id", "name", "avg_score", "score_trend", "failed_count", "logins_7d", "risk_score", "risk_category"]
    if not Path(db_path).exists():
        return pd.DataFrame(columns=columns)
    with sqlite3.connect(db_path) as connection:
        students = connection.execute("SELECT student_id, name FROM students ORDER BY student_id").fetchall()
    if not students:
        return pd.DataFrame(columns=columns)
    rows = []
    for student_id, name in students:
        features = calculate_features(db_path, student_id)
        risk = calculate_risk_score(features)
        category = "High Risk" if risk >= 70 else "Medium Risk" if risk >= 40 else "Low Risk"
        rows.append({"student_id": student_id, "name": name, **features, "risk_score": risk, "risk_category": category})
    return pd.DataFrame(rows, columns=columns).sort_values("risk_score", ascending=False).reset_index(drop=True)

