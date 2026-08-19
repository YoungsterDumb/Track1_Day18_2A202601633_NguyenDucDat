"""Unit tests for the Vietnamese explanation templates."""

from ews_shared import explain


def test_high_risk_lists_every_firing_rule(features_high):
    row = {**features_high, "risk_score": 75, "risk_category": "High Risk"}
    text = explain(row, rank=1)
    assert text.startswith("Xếp hạng #1 với 75/100")
    assert "dưới ngưỡng đạt" in text
    assert "giảm mạnh" in text
    assert "3 bài kiểm tra dưới 5 điểm" in text
    assert "1 lần đăng nhập" in text
    assert text.endswith("Cần liên hệ phụ huynh và sắp xếp hỗ trợ ngay trong tuần này.")


def test_clean_student_says_no_warning(features_low):
    row = {**features_low, "risk_score": 0, "risk_category": "Low Risk"}
    text = explain(row, rank=50)
    assert "không có tín hiệu cảnh báo nào" in text
    assert "Duy trì theo dõi định kỳ." in text


def test_medium_risk_uses_medium_next_step():
    row = {"avg_score": 6.5, "score_trend": -0.38, "failed_count": 0, "logins_7d": 4,
           "risk_score": 42, "risk_category": "Medium Risk"}
    text = explain(row, rank=13)
    assert "Nên theo dõi sát" in text
    assert "chỉ ở mức trung bình" in text


def test_explanation_stays_within_two_sentences():
    row = {"avg_score": 4.0, "score_trend": -0.9, "failed_count": 4, "logins_7d": 0,
           "risk_score": 75, "risk_category": "High Risk"}
    text = explain(row, rank=1)
    # Sentences are separated by ". "; decimals such as "4.0" carry no trailing space.
    assert text.count(". ") <= 1
    assert text.endswith(".")
