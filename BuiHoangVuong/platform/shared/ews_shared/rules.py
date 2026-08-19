"""Rule weights copied verbatim from the prototype's scoring.py."""

from typing import Dict

HIGH_THRESHOLD = 70
MEDIUM_THRESHOLD = 40


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


def categorize(risk_score: int) -> str:
    """Map a risk score onto the High/Medium/Low band used by the UI."""
    if risk_score >= HIGH_THRESHOLD:
        return "High Risk"
    return "Medium Risk" if risk_score >= MEDIUM_THRESHOLD else "Low Risk"
