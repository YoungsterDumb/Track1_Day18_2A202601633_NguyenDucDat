"""Unit tests for the shared rule engine (no database, no network)."""

import pytest

from ews_shared import build_features, calculate_risk_score, categorize
from ews_shared.features import failed_of, trend_of


def test_worst_case_scores_75(features_high):
    assert calculate_risk_score(features_high) == 75
    assert categorize(75) == "High Risk"


def test_healthy_student_scores_zero(features_low):
    assert calculate_risk_score(features_low) == 0
    assert categorize(0) == "Low Risk"


@pytest.mark.parametrize(
    ("features", "expected"),
    [
        ({"avg_score": 6.5, "score_trend": -0.38, "failed_count": 0, "logins_7d": 4}, 42),
        ({"avg_score": 4.9, "score_trend": 0.0, "failed_count": 1, "logins_7d": 9}, 27),
        ({"avg_score": 9.0, "score_trend": -0.10, "failed_count": 0, "logins_7d": 2}, 27),
    ],
)
def test_additive_weights(features, expected):
    assert calculate_risk_score(features) == expected


def test_category_boundaries():
    assert categorize(70) == "High Risk"
    assert categorize(69) == "Medium Risk"
    assert categorize(40) == "Medium Risk"
    assert categorize(39) == "Low Risk"


def test_build_features_matches_manual_math():
    features = build_features([8.0, 7.0, 6.0, 4.0], logins_7d=3)
    assert features == {"avg_score": 6.25, "score_trend": -1.33, "failed_count": 1, "logins_7d": 3}


def test_trend_and_failed_helpers():
    assert trend_of([5.0, 4.0, 3.0]) == pytest.approx(-1.0)
    assert trend_of([5.0]) == 0.0
    assert failed_of([4.9, 5.0, 2.0]) == 2


def test_build_features_rejects_empty_history():
    with pytest.raises(ValueError, match="At least one assessment"):
        build_features([], logins_7d=0)
