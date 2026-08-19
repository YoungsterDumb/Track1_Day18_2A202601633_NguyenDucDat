"""SQLite setup and reproducible sample-data generation."""

from datetime import datetime, timedelta
import random
import sqlite3
from pathlib import Path
from typing import Union

DbPath = Union[str, Path]


def init_db(db_path: DbPath = "students.db") -> None:
    """Create the students, assessments, and logins tables if needed."""
    with sqlite3.connect(db_path) as connection:
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS students (
                student_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS assessments (
                assessment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                assessment_no INTEGER NOT NULL,
                score REAL NOT NULL,
                FOREIGN KEY (student_id) REFERENCES students(student_id)
            );
            CREATE TABLE IF NOT EXISTS logins (
                login_id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                login_time TEXT NOT NULL,
                FOREIGN KEY (student_id) REFERENCES students(student_id)
            );
            """
        )


def load_sample_data(db_path: DbPath = "students.db") -> None:
    """Replace database contents with 50 deterministic synthetic students."""
    random.seed(42)
    init_db(db_path)
    now = datetime.now()
    with sqlite3.connect(db_path) as connection:
        connection.executescript(
            "DELETE FROM logins; DELETE FROM assessments; DELETE FROM students;"
        )
        for student_id in range(1, 51):
            name = f"Student {student_id:02d}"
            connection.execute(
                "INSERT INTO students(student_id, name, email) VALUES (?, ?, ?)",
                (student_id, name, f"student{student_id:02d}@example.edu"),
            )
            base_score = random.uniform(4.0, 9.5)
            trend = random.choice([-0.55, -0.3, -0.12, 0.0, 0.12, 0.25])
            for assessment_no in range(4):
                score = max(0.0, min(10.0, base_score + trend * assessment_no + random.uniform(-0.45, 0.45)))
                connection.execute(
                    "INSERT INTO assessments(student_id, assessment_no, score) VALUES (?, ?, ?)",
                    (student_id, assessment_no + 1, round(score, 2)),
                )
            login_count = random.randint(10, 30)
            activity_days = random.choice([7, 14, 30, 45])
            for _ in range(login_count):
                days_ago = random.uniform(0, activity_days)
                login_time = now - timedelta(days=days_ago)
                connection.execute(
                    "INSERT INTO logins(student_id, login_time) VALUES (?, ?)",
                    (student_id, login_time.isoformat(timespec="seconds")),
                )

