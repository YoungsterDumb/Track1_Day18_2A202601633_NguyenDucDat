"""Mock 'school system' sync: deterministic students across three risk profiles."""

from datetime import datetime, timedelta
import random
import sqlite3
from typing import Dict, List, Tuple

from database import DbPath, init_db

# profile -> (count, base score range, per-assessment trend range, logins in last 7 days)
PROFILES: Dict[str, Tuple[int, Tuple[float, float], Tuple[float, float], Tuple[int, int]]] = {
    "high": (10, (4.8, 5.6), (-0.80, -0.60), (0, 2)),
    "mid": (15, (6.2, 7.2), (-0.45, -0.30), (3, 4)),
    "low": (25, (7.8, 9.5), (0.00, 0.25), (8, 20)),
}


def sync_school_data(db_path: DbPath = "students.db", seed: int = 2026) -> Dict[str, int]:
    """Replace the database with 50 synthetic students and return the profile mix."""
    random.seed(seed)
    init_db(db_path)
    now = datetime.now()
    roster: List[str] = [name for name, cfg in PROFILES.items() for _ in range(cfg[0])]
    random.shuffle(roster)

    with sqlite3.connect(db_path) as connection:
        connection.executescript("DELETE FROM logins; DELETE FROM assessments; DELETE FROM students;")
        for student_id, profile in enumerate(roster, start=1):
            _, base_range, trend_range, recent_range = PROFILES[profile]
            connection.execute(
                "INSERT INTO students(student_id, name, email) VALUES (?, ?, ?)",
                (student_id, f"Học sinh {student_id:02d}", f"hs{student_id:02d}@truong.edu.vn"),
            )
            base = random.uniform(*base_range)
            trend = random.uniform(*trend_range)
            for assessment_no in range(4):
                score = max(0.0, min(10.0, base + trend * assessment_no + random.uniform(-0.3, 0.3)))
                connection.execute(
                    "INSERT INTO assessments(student_id, assessment_no, score) VALUES (?, ?, ?)",
                    (student_id, assessment_no + 1, round(score, 2)),
                )
            recent = random.randint(*recent_range)
            older = random.randint(3, 12)
            for days_ago in [random.uniform(0, 5.5) for _ in range(recent)] + [random.uniform(8, 45) for _ in range(older)]:
                connection.execute(
                    "INSERT INTO logins(student_id, login_time) VALUES (?, ?)",
                    (student_id, (now - timedelta(days=days_ago)).isoformat(timespec="seconds")),
                )
    return {profile: cfg[0] for profile, cfg in PROFILES.items()}
