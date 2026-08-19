"""
VLearn micro-prototype — SHARED FIXTURE & COMPONENTS (bản Streamlit)

Cả ba option đọc nội dung từ đúng module này, nên không option nào có thể
lệch content, context hay task so với hai option kia (Comparison Contract,
Design Sheet §2.2).

Nội dung ở đây PHẢI khớp với prototype/shared.js — nếu sửa một bên thì sửa cả hai.
"""

import streamlit as st

FIXTURE = {
    "course":  "AI Foundation · Module 4 — Biểu diễn văn bản",
    "session": "Buổi 12 (live) đã kết thúc lúc 20:30 hôm nay",
    "clock":   "21:47",
    "slide_no": 14,
    "slide_total": 22,
    "slide_title": "Chuẩn hoá trọng số TF-IDF",
    "paras": [
        {"id": "p1", "kind": "text", "md":
            "Trọng số của một từ **t** trong văn bản **d** không chỉ phụ thuộc vào việc t "
            "xuất hiện bao nhiêu lần trong d, mà còn phụ thuộc vào việc t hiếm hay phổ biến "
            "trên toàn bộ tập văn bản."},
        {"id": "p2", "kind": "text", "md":
            "Ký hiệu: **tf(t,d)** = số lần t xuất hiện trong d · **df(t)** = số văn bản có "
            "chứa t · **n** = tổng số văn bản trong tập."},
        {"id": "p3", "kind": "formula", "md":
            "Khi smooth_idf = True:\n\n"
            "    idf(t) = log( (1 + n) / (1 + df(t)) ) + 1\n"
            "    w(t,d) = tf(t,d) × idf(t)\n\n"
            "Sau đó mỗi vector văn bản được chuẩn hoá theo chuẩn L2."},
        {"id": "p4", "kind": "text", "md":
            "Vì phép chuẩn hoá L2 diễn ra **sau** khi nhân, hai văn bản có cùng tỉ lệ từ "
            "nhưng khác độ dài sẽ cho ra **cùng một vector**. Đây là lý do độ dài văn bản "
            "không còn ảnh hưởng tới cosine similarity."},
        {"id": "p5", "kind": "text", "md":
            "**Bài tập cuối slide:** giải thích vì sao số **+1** ở cuối công thức idf khiến "
            "không từ nào có trọng số bằng 0, kể cả từ xuất hiện trong mọi văn bản."},
    ],
    # Task nói KẾT QUẢ cần đạt, không nói nút cần bấm. Giống hệt nhau ở A/B/C.
    "task": ("Làm sao để **bạn không phải bỏ qua đoạn mình chưa hiểu**, và để "
             "**chỗ bạn đang mắc đến được người có thể giúp bạn**."),
}

PARA_LABEL = {p["id"]: ("khối công thức" if p["kind"] == "formula" else "đoạn văn")
              for p in FIXTURE["paras"]}


# --------------------------------------------------------------------------
# CSS dùng chung
# --------------------------------------------------------------------------
def inject_css():
    st.markdown("""
    <style>
      .block-container{padding-top:2.2rem;max-width:900px}
      #MainMenu, footer, header {visibility:hidden}

      .ctxstrip{background:#fff8e6;border:1px solid #f0e0b8;border-radius:9px;
        padding:10px 14px;font-size:13.5px;color:#6b5518;margin-bottom:6px}
      .ctxstrip b{color:#4a3a0d}

      .optbadge{display:inline-block;background:#16181d;color:#fff;border-radius:999px;
        padding:3px 11px;font-size:11.5px;font-weight:700;letter-spacing:.06em}

      .slidecard{background:#fff;border:1px solid #e2e5ea;border-radius:10px;padding:4px 6px 2px}
      .formula{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:13px;
        background:#f7f8fa;border:1px solid #e2e5ea;border-radius:8px;
        padding:12px 14px;white-space:pre-wrap;color:#16181d}

      .quoteblock{border-left:3px solid #1f5fd8;background:#eaf0fd;padding:10px 14px;
        border-radius:0 8px 8px 0;font-size:13.5px;color:#213a63}

      .aibox{border:1px solid #cfe0fb;background:#f7faff;border-radius:10px;padding:14px 16px}
      .evidence{margin-top:10px;padding-top:10px;border-top:1px dashed #cfe0fb;
        font-size:12.5px;color:#5b616e}

      .tag{display:inline-block;font-size:11.5px;border-radius:999px;padding:2px 9px;
        border:1px solid transparent;margin-right:5px}
      .tag.ai{background:#eaf0fd;color:#1a4aa8;border-color:#cfe0fb}
      .tag.ok{background:#e7f5ef;color:#0f7a52;border-color:#c6e6d8}
      .tag.warn{background:#fdf3e2;color:#b06a00;border-color:#f0dcb4}
      .tag.stop{background:#fdeceb;color:#b3261e;border-color:#f0cfcc}
      .tag.mute{background:#f1f2f5;color:#5b616e;border-color:#e2e5ea}

      .rowitem{border:1px solid #e2e5ea;border-radius:10px;padding:14px 16px;background:#fff}
      .sig{font-size:12.5px;color:#5b616e;margin:3px 0 3px 14px}
      .mebubble{background:#16181d;color:#fff;border-radius:14px 14px 3px 14px;
        padding:9px 14px;font-size:14px;display:inline-block;max-width:78%}
      .small{font-size:12.5px;color:#8b909c}
      .notice{border-radius:9px;padding:11px 14px;font-size:13.5px}
      .notice.info{background:#eaf0fd;color:#1a4aa8}
      .notice.warn{background:#fdf3e2;color:#b06a00}
      .notice.ok{background:#e7f5ef;color:#0f7a52}
      .notice.mute{background:#f1f2f5;color:#5b616e}
    </style>
    """, unsafe_allow_html=True)


# --------------------------------------------------------------------------
# Thanh trên + dải context: giống hệt nhau ở cả ba option
# --------------------------------------------------------------------------
def shell(option_letter: str, on_reset):
    c1, c2, c3 = st.columns([0.52, 0.20, 0.28])
    with c1:
        st.markdown(f"**VLearn** · <span class='small'>{FIXTURE['course']}</span>",
                    unsafe_allow_html=True)
    with c2:
        st.markdown(f"<span class='optbadge'>PHƯƠNG ÁN {option_letter}</span>",
                    unsafe_allow_html=True)
    with c3:
        if st.button("↺ Về màn hình chung", key=f"reset_{option_letter}",
                     use_container_width=True):
            on_reset()

    st.markdown(
        f"<div class='ctxstrip'><b>{FIXTURE['clock']}</b> — buổi live đã kết thúc, bạn đang "
        f"tự xem lại slide {FIXTURE['slide_no']}/{FIXTURE['slide_total']}. Giảng viên không "
        f"online. &nbsp;·&nbsp; <b>Việc cần đạt:</b> không phải bỏ qua đoạn chưa hiểu, và để "
        f"chỗ đang mắc đến được người có thể giúp.</div>",
        unsafe_allow_html=True)


# --------------------------------------------------------------------------
# Slide fixture — dùng chung, nội dung không đổi
#   affordance: None, hoặc (label, key_prefix, side) với side in {'left','right'}
#   Trả về id của đoạn được bấm, hoặc None.
# --------------------------------------------------------------------------
def render_slide(affordance=None):
    clicked = None
    st.markdown(f"#### {FIXTURE['slide_title']}")
    st.caption(f"Slide {FIXTURE['slide_no']}/{FIXTURE['slide_total']} · "
               f"◀ Slide 13: Ma trận document–term · Slide 15: Cosine similarity ▶")

    for p in FIXTURE["paras"]:
        if affordance is None:
            _para_body(p)
            continue

        label, key_prefix, side = affordance
        if side == "left":
            c_btn, c_txt = st.columns([0.10, 0.90])
            with c_btn:
                if st.button(label, key=f"{key_prefix}_{p['id']}", help="Đánh dấu đoạn này"):
                    clicked = p["id"]
            with c_txt:
                _para_body(p)
        else:
            c_txt, c_btn = st.columns([0.80, 0.20])
            with c_txt:
                _para_body(p)
            with c_btn:
                if st.button(label, key=f"{key_prefix}_{p['id']}", use_container_width=True):
                    clicked = p["id"]
        st.write("")
    return clicked


def _para_body(p):
    if p["kind"] == "formula":
        st.markdown(f"<div class='formula'>{p['md']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(p["md"])


def para_md(para_id: str) -> str:
    return next(p["md"] for p in FIXTURE["paras"] if p["id"] == para_id)
