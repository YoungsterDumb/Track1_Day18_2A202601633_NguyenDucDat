"""Storage-agnostic feature extraction (the prototype's calculate_features, minus SQLite)."""

from typing import Dict, Sequence


def trend_of(scores: Sequence[float]) -> float:
    """Average change per assessment, first to last."""
    return (scores[-1] - scores[0]) / max(len(scores) - 1, 1)


def failed_of(scores: Sequence[float]) -> int:
    """Number of assessments below the pass mark of 5."""
    return int(sum(score < 5 for score in scores))


def build_features(scores: Sequence[float], logins_7d: int) -> Dict[str, float]:
    """Return the four features the risk rules consume."""
    if not scores:
        raise ValueError("At least one assessment score is required.")
    return {
        "avg_score": round(sum(scores) / len(scores), 2),
        "score_trend": round(trend_of(scores), 2),
        "failed_count": failed_of(scores),
        "logins_7d": int(logins_7d),
    }
