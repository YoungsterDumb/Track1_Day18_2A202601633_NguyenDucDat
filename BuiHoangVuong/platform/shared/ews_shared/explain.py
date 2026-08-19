"""Rule-derived, plain-Vietnamese explanation of a student's rank."""

from typing import Dict, List

# (predicate, weight, Vietnamese reason) — mirrors calculate_risk_score in scoring.py.
REASON_RULES = [
    (lambda r: r["avg_score"] < 5, 20, "điểm trung bình {avg_score}/10 dưới ngưỡng đạt"),
    (lambda r: 5 <= r["avg_score"] < 7, 10, "điểm trung bình {avg_score}/10 chỉ ở mức trung bình"),
    (lambda r: r["score_trend"] < -0.15, 25, "điểm giảm mạnh {score_trend} mỗi bài kiểm tra"),
    (lambda r: -0.15 <= r["score_trend"] < -0.05, 12, "điểm có xu hướng giảm nhẹ"),
    (lambda r: r["failed_count"] >= 2, 15, "{failed_count} bài kiểm tra dưới 5 điểm"),
    (lambda r: r["failed_count"] == 1, 7, "1 bài kiểm tra dưới 5 điểm"),
    (lambda r: r["logins_7d"] < 3, 15, "chỉ {logins_7d} lần đăng nhập trong 7 ngày qua"),
    (lambda r: 3 <= r["logins_7d"] < 5, 7, "{logins_7d} lần đăng nhập trong 7 ngày qua, thấp hơn bình thường"),
]

NEXT_STEP = {
    "High Risk": "Cần liên hệ phụ huynh và sắp xếp hỗ trợ ngay trong tuần này.",
    "Medium Risk": "Nên theo dõi sát và nhắc nhở trong 2 tuần tới.",
    "Low Risk": "Duy trì theo dõi định kỳ.",
}


def explain(row: Dict[str, object], rank: int) -> str:
    """Explain a student's rank in 1-2 plain Vietnamese sentences, derived from the rules."""
    reasons: List[str] = [
        template.format(**row) for predicate, _, template in REASON_RULES if predicate(row)
    ]
    if not reasons:
        return f"Xếp hạng #{rank} với {row['risk_score']}/100 điểm rủi ro: không có tín hiệu cảnh báo nào. {NEXT_STEP[row['risk_category']]}"
    return (
        f"Xếp hạng #{rank} với {row['risk_score']}/100 điểm rủi ro, chủ yếu do {', '.join(reasons)}. "
        f"{NEXT_STEP[row['risk_category']]}"
    )
