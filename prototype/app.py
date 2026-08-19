"""
VLearn — ba micro-prototype A/B/C (bản Streamlit)

Nhóm Mái Ấm Gia Đình · Case C — AI Support Radar · Track 1 Day 18

Chạy:  streamlit run app.py

Cả ba option dùng chung fixture.py (context · content · task · components).
Chỉ critical interaction là khác. Xem three-option-design-sheet.md §2.2.
"""

import time
import streamlit as st

from fixture import FIXTURE, PARA_LABEL, inject_css, para_md, render_slide, shell

st.set_page_config(page_title="VLearn — Prototype A/B/C", page_icon="📘",
                   layout="centered", initial_sidebar_state="collapsed")
inject_css()

# ---------------------------------------------------------------- state ----
DEFAULTS = {
    "screen": "hub",
    # Option A
    "a_step": 1, "a_para": None, "a_kind": None, "a_vis": "self",
    "a_text": "", "a_ai": "",
    # Option B
    "b_step": 1, "b_para": None, "b_log": [], "b_dropped": set(), "b_extra": "",
    # Option C
    "c_step": 1, "c_t0": None, "c_removed": set(), "c_pulled": False,
}
for k, v in DEFAULTS.items():
    st.session_state.setdefault(k, v.copy() if isinstance(v, (set, list, dict)) else v)


def go_hub():
    """Reset về màn hình chung — có ở mọi option (Definition of testable)."""
    for k, v in DEFAULTS.items():
        st.session_state[k] = v.copy() if isinstance(v, (set, list, dict)) else v
    st.rerun()


def open_option(letter):
    st.session_state.screen = letter
    if letter == "c":
        st.session_state.c_t0 = time.time()   # bắt đầu đo phiên xem lại thật
    st.rerun()


def fmt_secs(s):
    s = max(8, int(round(s)))
    return f"{s // 60} phút {s % 60} giây" if s >= 60 else f"{s} giây"


# ================================================================== HUB ====
def screen_hub():
    st.markdown("**VLearn** · <span class='small'>Micro-prototype A/B/C · "
                "Nhóm Mái Ấm Gia Đình · Day 18</span>", unsafe_allow_html=True)
    st.title("Tình huống của bạn")
    st.caption("Ba phương án dưới đây bắt đầu từ đúng một tình huống và đúng một việc "
               "cần đạt. Bạn tự thao tác; không có câu trả lời đúng hay sai.")

    st.markdown("##### Bối cảnh")
    st.caption("Giống hệt nhau ở cả ba phương án.")
    st.markdown(
        f"<div class='notice info'><b>{FIXTURE['clock']} tối nay.</b> Buổi live số 12 của môn "
        f"<b>{FIXTURE['course']}</b> đã kết thúc lúc 20:30. Bạn đang ngồi một mình xem lại "
        f"slide <b>{FIXTURE['slide_no']}/{FIXTURE['slide_total']} — \"{FIXTURE['slide_title']}\"</b>. "
        "Có một đoạn bạn đọc đi đọc lại mà vẫn chưa thông. Giảng viên không online. "
        "Tuần sau có bài nộp dùng đúng phần này.</div>", unsafe_allow_html=True)

    st.markdown("##### Việc bạn cần đạt")
    st.caption("Giống hệt nhau ở cả ba phương án.")
    st.markdown(f"<div class='quoteblock'>{FIXTURE['task']}</div>", unsafe_allow_html=True)

    st.markdown("##### Nội dung bạn đang xem")
    st.caption("Cả ba phương án dùng đúng slide này, không đổi một chữ.")
    with st.container(border=True):
        render_slide(None)

    st.markdown("### Ba phương án")
    st.caption("Bạn sẽ dùng lần lượt cả ba. Sau mỗi phương án, quay lại đây bằng nút "
               "**↺ Về màn hình chung** ở góc phải trên.")

    c1, c2, c3 = st.columns(3)
    for col, letter, desc in [
        (c1, "a", "Bạn tự đánh dấu chỗ mình đang mắc trên slide và tự chọn ai được nhìn thấy nó."),
        (c2, "b", "Bạn hỏi ngay tại đoạn slide đó và nhận câu trả lời trong bài học."),
        (c3, "c", "Bạn cứ xem lại bài như bình thường, rồi xem hệ thống đưa ra gì ở cuối phiên."),
    ]:
        with col, st.container(border=True):
            st.markdown(f"### {letter.upper()}")
            st.caption(desc)
            if st.button(f"Mở phương án {letter.upper()} →", key=f"open_{letter}",
                         use_container_width=True):
                open_option(letter)

    st.caption("Prototype dùng cho buổi test — nội dung phản hồi là dữ liệu mẫu dựng sẵn, "
               "không phải mô hình thật.")


# ============================================================= OPTION A ====
# Cơ chế: học viên TỰ TUYÊN BỐ chỗ mắc. AI không suy đoán gì (Don't Act).
VIS_TEXT = {
    "self":    "Chỉ mình bạn nhìn thấy. Chưa ai được báo.",
    "teacher": "Giảng viên và lab coach nhìn thấy đoạn này kèm tên bạn. "
               "Bạn không phải nhắn tin cho ai.",
    "class":   "Cả lớp thấy \"có người đang mắc ở đoạn này\". Tên bạn không hiện ra.",
}
VIS_LABEL = {
    "self":    "Chỉ mình tôi — dùng như một chỗ đánh dấu để quay lại. Không ai khác thấy.",
    "teacher": "Giảng viên và lab coach — hai người thấy đúng đoạn này, kèm tên bạn. "
               "Bạn không phải nhắn tin cho ai.",
    "class":   "Cả lớp — ẩn danh. Bạn cùng lớp thấy \"có người đang mắc ở đoạn này\", "
               "không thấy tên bạn.",
}


def screen_a():
    shell("A", go_hub)
    step = st.session_state.a_step

    # ---- state 1: slide + affordance -------------------------------------
    if step == 1:
        with st.container(border=True):
            clicked = render_slide(("⚑", "amark", "left"))
        st.caption("Mẹo: mỗi đoạn trên slide có một ô nhỏ ở lề trái.")
        if clicked:
            st.session_state.a_para = clicked
            st.session_state.a_step = 2
            st.rerun()

    # ---- state 2: soạn đánh dấu (critical interaction) --------------------
    elif step == 2:
        st.markdown("#### Đánh dấu chỗ bạn đang mắc")
        st.caption("Chỗ đánh dấu gắn thẳng vào đoạn slide bên dưới.")
        st.markdown(f"<div class='quoteblock'><b>Đoạn bạn đang đánh dấu — slide 14:</b><br>"
                    f"{para_md(st.session_state.a_para)}</div>", unsafe_allow_html=True)

        st.markdown("**Bạn đang mắc kiểu gì?** — chọn nhanh, hoặc bỏ trống")
        kinds = ["— không ghi loại —", "Không hiểu một thuật ngữ",
                 "Không hiểu vì sao ra kết quả này", "Hiểu chữ nhưng không áp dụng được"]
        kind = st.radio("kind", kinds, index=0, horizontal=False, label_visibility="collapsed")

        st.markdown("**Bạn muốn viết thêm gì không?** — không bắt buộc, có thể gửi khi để trống")
        note = st.text_area(
            "note", value=st.session_state.a_text, height=90, label_visibility="collapsed",
            placeholder="Ví dụ: mình không hiểu vì sao chuẩn hoá sau khi nhân lại làm mất "
                        "ảnh hưởng của độ dài.")

        # AI ở đây chỉ ASK, không bao giờ ACT
        c1, c2 = st.columns([0.34, 0.66])
        with c1:
            if st.button("✨ Nhờ AI gợi ý cách diễn đạt", use_container_width=True):
                typed = note.strip()
                st.session_state.a_ai = (
                    f"Mình chưa rõ ở đoạn này: {typed} Cụ thể mình đang vướng ở bước chuẩn "
                    "hoá L2 sau khi nhân tf với idf." if typed else
                    "Ở slide 14, mình chưa hiểu vì sao khi chuẩn hoá L2 sau bước nhân tf × idf "
                    "thì hai văn bản khác độ dài lại cho ra cùng một vector. Mình đang kẹt ở "
                    "chỗ nào là nguyên nhân?")
                st.session_state.a_text = note
                st.rerun()
        with c2:
            st.caption("AI chỉ viết lại câu chữ. AI không tự tạo đánh dấu và không đọc "
                       "hành vi học của bạn.")

        if st.session_state.a_ai:
            st.markdown(
                f"<div class='aibox'><span class='tag ai'>✨ AI gợi ý</span> "
                f"<span class='small'>Dựa trên: đoạn slide bạn đã chọn + phần bạn vừa gõ. "
                f"Không dùng dữ liệu nào khác.</span><br><br>{st.session_state.a_ai}</div>",
                unsafe_allow_html=True)
            d1, d2, _ = st.columns([0.22, 0.24, 0.54])
            with d1:
                if st.button("Dùng câu này", type="primary", use_container_width=True):
                    st.session_state.a_text = st.session_state.a_ai
                    st.session_state.a_ai = ""
                    st.rerun()
            with d2:
                if st.button("Bỏ, tôi tự viết", use_container_width=True):
                    st.session_state.a_ai = ""
                    st.session_state.a_text = note
                    st.rerun()

        st.markdown("**Ai được nhìn thấy đánh dấu này?** — bạn quyết định, "
                    "mặc định là chỉ mình bạn")
        vis = st.radio("vis", ["self", "teacher", "class"],
                       format_func=lambda k: VIS_LABEL[k],
                       index=["self", "teacher", "class"].index(st.session_state.a_vis),
                       label_visibility="collapsed")

        st.divider()
        c1, c2, _ = st.columns([0.20, 0.26, 0.54])
        with c1:
            if st.button("Đặt đánh dấu", type="primary", use_container_width=True):
                st.session_state.a_kind = None if kind.startswith("—") else kind
                st.session_state.a_text = note
                st.session_state.a_vis = vis
                st.session_state.a_step = 3
                st.rerun()
        with c2:
            if st.button("Huỷ, quay lại slide", use_container_width=True):
                st.session_state.a_step = 1
                st.rerun()

    # ---- state 3: kết quả + đường lấy lại control -------------------------
    else:
        vis = st.session_state.a_vis
        st.markdown(f"<div class='notice ok'><b>Đã đặt đánh dấu.</b> {VIS_TEXT[vis]}</div>",
                    unsafe_allow_html=True)
        st.markdown("#### Đánh dấu của bạn")
        kind_tag = (f"<span class='tag mute'>{st.session_state.a_kind}</span>"
                    if st.session_state.a_kind else
                    "<span class='tag mute'>không ghi loại</span>")
        vis_tag = ("<span class='tag mute'>riêng tư</span>" if vis == "self" else
                   f"<span class='tag ok'>"
                   f"{'giảng viên + coach' if vis == 'teacher' else 'cả lớp · ẩn danh'}</span>")
        body = (f"\"{st.session_state.a_text}\"" if st.session_state.a_text.strip()
                else "<i>Bạn không viết gì thêm — đánh dấu vẫn gửi được.</i>")
        st.markdown(
            f"<div class='rowitem'><b>Slide 14 · {PARA_LABEL[st.session_state.a_para]}</b><br>"
            f"{kind_tag}{vis_tag}<span class='tag warn'>chưa ai xem</span><br><br>"
            f"<span class='small'>{body}</span></div>", unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("Sửa nội dung", use_container_width=True):
                st.session_state.a_step = 2
                st.rerun()
        with c2:
            if st.button("Đổi người được xem", use_container_width=True):
                st.session_state.a_step = 2
                st.rerun()
        with c3:
            if st.button("Gỡ đánh dấu này", use_container_width=True):
                st.toast("Đã gỡ đánh dấu. Không ai còn nhìn thấy nó.")
                st.session_state.a_step = 1
                st.rerun()

        st.divider()
        st.markdown("#### Rồi sao nữa?")
        st.caption("Bạn không phải chờ ở đây.")
        c1, c2, _ = st.columns([0.22, 0.26, 0.52])
        with c1:
            if st.button("Đi tiếp slide 15", type="primary", use_container_width=True):
                st.toast("Bạn đã đi tiếp — đánh dấu vẫn nằm ở slide 14")
        with c2:
            if st.button("Quay lại slide 14", use_container_width=True):
                st.session_state.a_step = 1
                st.rerun()


# ============================================================= OPTION B ====
# Cơ chế: AI giải thích tại chỗ (Act), rồi HỎI trước khi chuyển cho người thật (Ask).
ANSWER_1 = """<span class='tag ai'>✨ Trợ lý bài học</span>
<span class='tag ok'>Khá chắc — phần này có trong slide buổi 12</span><br><br>
Thứ tự phép tính là điểm mấu chốt. Trọng số <b>w = tf × idf</b> được tính trước, lúc này
văn bản dài vẫn có tf lớn hơn. Chuẩn hoá L2 sau đó chia cả vector cho độ dài của chính nó,
nên phần "dài hơn" bị chia mất. Cái còn lại là <b>tỉ lệ giữa các từ</b>, không phải số lượng từ.
<div class='evidence'><b>Trợ lý dựa vào:</b><ul>
<li>Slide 14, khối công thức và đoạn ngay sau nó</li>
<li>Slide 9 — định nghĩa df(t) và n</li>
<li>Ghi chú buổi 12, phút 41:20 — giảng viên nhắc "chuẩn hoá là bước cuối"</li>
</ul></div>"""

ANSWER_2 = """<span class='tag ai'>✨ Trợ lý bài học</span>
<span class='tag warn'>Không chắc — phần này không nằm trong tài liệu buổi 12</span><br><br>
Mình chỉ đọc được slide và ghi chú của buổi 12. Đề bài nộp tuần sau <b>không có trong đó</b>,
nên nếu mình trả lời tiếp thì là mình đang đoán.
<div class='evidence'><b>Mình đã tìm ở:</b><ul>
<li>Slide 1–22 buổi 12 — không có mô tả bài nộp</li>
<li>Ghi chú buổi 12 — không có phần giao bài</li>
</ul></div>"""

SEND_ITEMS = [("i1", "Đoạn slide 14 bạn đang hỏi"), ("i2", "Câu hỏi 1 của bạn"),
              ("i3", "Câu hỏi 2 của bạn"), ("i4", "Tên và lớp của bạn")]


def screen_b():
    shell("B", go_hub)
    step = st.session_state.b_step

    # ---- state 1 ---------------------------------------------------------
    if step == 1:
        with st.container(border=True):
            clicked = render_slide(("Hỏi về đoạn này", "bask", "right"))
        if clicked:
            st.session_state.b_para = clicked
            st.session_state.b_step = 2
            st.rerun()

    # ---- state 2: hỏi tại chỗ (critical interaction) ---------------------
    elif step == 2:
        st.markdown("#### Hỏi về đoạn này")
        st.caption("Câu hỏi của bạn được gắn với đúng đoạn slide bên dưới.")
        st.markdown(f"<div class='quoteblock'><b>Đoạn bạn đang hỏi — slide 14:</b><br>"
                    f"{para_md(st.session_state.b_para)}</div>", unsafe_allow_html=True)
        st.markdown("<div class='notice mute'><b>Trợ lý bài học</b> chỉ đọc slide và tài liệu "
                    "của buổi 12. Nó <b>không biết bài nộp tuần sau</b> và <b>có thể trả lời "
                    "sai</b>. Khi nó không chắc, nó sẽ nói ra.</div>", unsafe_allow_html=True)
        st.write("")

        for role, content in st.session_state.b_log:
            if role == "me":
                st.markdown(f"<div style='text-align:right'><span class='mebubble'>"
                            f"{content}</span></div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='aibox'>{content}</div>", unsafe_allow_html=True)
            st.write("")

        # Khoảnh khắc AI ASK — chỉ hiện sau lượt trả lời thứ hai
        if len(st.session_state.b_log) >= 4:
            st.markdown("**Bạn có muốn mình chuyển câu hỏi này cho giảng viên không?** "
                        "Mình sẽ gửi kèm đoạn slide và những câu bạn đã hỏi, để bạn không "
                        "phải kể lại từ đầu.")
            c1, c2, c3 = st.columns([0.34, 0.24, 0.24])
            with c1:
                if st.button("Xem trước rồi chuyển giúp tôi", type="primary",
                             use_container_width=True):
                    st.session_state.b_step = 25
                    st.rerun()
            with c2:
                if st.button("Để tôi tự hỏi", use_container_width=True):
                    st.toast("Trợ lý dừng lại. Không có gì được gửi đi.")
            with c3:
                if st.button("Không, tôi thử tiếp", use_container_width=True):
                    st.toast("Được — bạn cứ hỏi tiếp.")
            st.divider()

        q = st.text_area("q", height=80, label_visibility="collapsed",
                         placeholder="Gõ câu hỏi của bạn…")
        c1, c2, c3, c4 = st.columns([0.20, 0.28, 0.30, 0.22])
        with c1:
            if st.button("Gửi câu hỏi", type="primary", use_container_width=True):
                _ask(q)
        with c2:
            if st.button("Vì sao chuẩn hoá sau khi nhân?", use_container_width=True):
                _ask("Vì sao chuẩn hoá L2 lại làm mất ảnh hưởng của độ dài văn bản?")
        with c3:
            if st.button("Vậy bài nộp tuần sau phải làm thế nào?", use_container_width=True):
                _ask("Vậy bài nộp tuần sau mình phải chuẩn hoá ở bước nào?")
        with c4:
            if st.button("Đóng, quay lại slide", use_container_width=True):
                st.session_state.b_step = 1
                st.rerun()

    # ---- state 2b: xem trước những gì sẽ được gửi ------------------------
    elif step == 25:
        st.markdown("#### Trước khi chuyển cho giảng viên")
        st.caption("Đây là **toàn bộ** những gì sẽ được gửi đi. Bỏ mục nào cũng được.")
        for iid, label in SEND_ITEMS:
            off = iid in st.session_state.b_dropped
            c1, c2 = st.columns([0.72, 0.28])
            with c1:
                st.markdown(f"<div class='rowitem' style='opacity:{0.4 if off else 1}'>"
                            f"{'~~' if off else ''}{label}{'~~' if off else ''}</div>",
                            unsafe_allow_html=True)
            with c2:
                if st.button("Thêm lại" if off else "Bỏ mục này", key=f"drop_{iid}",
                             use_container_width=True):
                    st.session_state.b_dropped.symmetric_difference_update({iid})
                    st.rerun()
        st.write("")
        extra = st.text_area("Muốn nói thêm với giảng viên? — không bắt buộc", height=70)
        st.divider()
        c1, c2, _ = st.columns([0.16, 0.30, 0.54])
        with c1:
            if st.button("Gửi", type="primary", use_container_width=True):
                st.session_state.b_extra = extra
                st.session_state.b_step = 3
                st.rerun()
        with c2:
            if st.button("Quay lại, tôi thử tiếp", use_container_width=True):
                st.session_state.b_step = 2
                st.rerun()

    # ---- state 3: kết quả ------------------------------------------------
    else:
        st.markdown("<div class='notice ok'><b>Đã chuyển cho giảng viên.</b> "
                    "Bạn không phải mở lời nhắn tin cho ai.</div>", unsafe_allow_html=True)
        kept = [lbl for iid, lbl in SEND_ITEMS if iid not in st.session_state.b_dropped]
        extra = st.session_state.b_extra.strip()
        # Dựng sẵn hai mảnh HTML ngoài f-string: Python 3.11 không cho phép dấu
        # backslash bên trong biểu thức f-string (PEP 701 chỉ nới từ 3.12).
        kept_html = "<br>".join(kept) if kept else "<i>bạn đã bỏ hết các mục</i>"
        extra_html = f'<br><br><b>Bạn nhắn thêm:</b> "{extra}"' if extra else ""
        st.markdown(
            f"<div class='rowitem'><b>Đã gửi tới: giảng viên buổi 12 + lab coach</b><br>"
            f"<span class='tag warn'>chưa ai xem</span>"
            f"<span class='tag mute'>gửi lúc 21:53</span><br><br>"
            f"<span class='small'><b>Nội dung đã gửi:</b><br>"
            f"{kept_html}{extra_html}</span></div>",
            unsafe_allow_html=True)

        c1, c2, _ = st.columns([0.26, 0.28, 0.46])
        with c1:
            if st.button("Thu hồi, đừng gửi nữa", use_container_width=True):
                st.toast("Đã thu hồi. Giảng viên không còn nhìn thấy gì.")
                st.session_state.b_step = 1
                st.rerun()
        with c2:
            if st.button("Sửa lại nội dung gửi", use_container_width=True):
                st.session_state.b_step = 25
                st.rerun()

        st.divider()
        st.markdown("#### Rồi sao nữa?")
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("Đi tiếp slide 15", type="primary", use_container_width=True):
                st.toast("Bạn đã đi tiếp — câu hỏi vẫn đang chờ trả lời")
        with c2:
            if st.button("Hỏi tiếp trợ lý", use_container_width=True):
                st.session_state.b_step = 2
                st.rerun()
        with c3:
            if st.button("Quay lại slide 14", use_container_width=True):
                st.session_state.b_step = 1
                st.rerun()


def _ask(text):
    if not text.strip():
        return
    st.session_state.b_log.append(("me", text))
    turn = sum(1 for r, _ in st.session_state.b_log if r == "me")
    st.session_state.b_log.append(("ai", ANSWER_1 if turn == 1 else ANSWER_2))
    st.rerun()


# ============================================================= OPTION C ====
# Cơ chế: AI suy ra từ hành vi thụ động và HÀNH ĐỘNG trước khi hỏi (Act).
def screen_c():
    shell("C", go_hub)
    step = st.session_state.c_step

    # ---- state 1: xem lại bài như bình thường ----------------------------
    if step == 1:
        st.markdown("<div class='notice mute'>🔴 <b>VLearn đang ghi nhận hoạt động ôn tập "
                    "của bạn</b> để tự tổng hợp những chỗ bạn nên xem lại.</div>",
                    unsafe_allow_html=True)
        c1, c2, _ = st.columns([0.22, 0.12, 0.66])
        with c1:
            detail = st.toggle("Ghi nhận những gì?")
        with c2:
            if st.button("Tắt", use_container_width=True):
                st.toast("Đã tắt cho phiên này. Danh sách cuối phiên sẽ không được tạo.")
        if detail:
            st.markdown("<div class='notice mute'>Thời gian bạn dừng ở từng đoạn · số lần "
                        "bạn quay lại một đoạn · thứ tự bạn đọc · bạn có mở phần bài tập cuối "
                        "slide không. <b>Không</b> ghi nội dung bạn gõ và <b>không</b> ghi "
                        "màn hình.</div>", unsafe_allow_html=True)

        with st.container(border=True):
            render_slide(None)

        c1, c2 = st.columns([0.26, 0.74])
        with c1:
            if st.button("Kết thúc phiên xem lại", type="primary", use_container_width=True):
                st.session_state.c_step = 2
                st.rerun()
        with c2:
            st.caption("Bạn cứ đọc slide như bình thường trước đã.")

    # ---- state 2: digest tự sinh (critical interaction) ------------------
    elif step == 2:
        elapsed = time.time() - (st.session_state.c_t0 or time.time())
        st.markdown("<span class='tag ai'>✨ VLearn tự tổng hợp</span> "
                    "<span class='small'>Bạn không phải hỏi gì. Danh sách này được tạo từ "
                    "hoạt động của bạn trong phiên vừa rồi.</span>", unsafe_allow_html=True)
        st.markdown("#### 3 chỗ bạn nên xem lại")
        st.markdown("<div class='notice warn'>Mục được đánh dấu <span class='tag stop'>đã gửi"
                    "</span> <b>đã được đưa vào danh sách hỗ trợ của giảng viên</b> khi phiên "
                    "kết thúc. Bạn có thể gỡ bên dưới.</div>", unsafe_allow_html=True)
        st.write("")

        for item in _c_items(elapsed):
            off = item["id"] in st.session_state.c_removed
            with st.container(border=True):
                sent = ("<span class='tag stop'>đã gửi cho giảng viên</span>"
                        if item["sent"] and not off else "<span class='tag mute'>chưa gửi</span>")
                st.markdown(
                    f"<div style='opacity:{0.45 if off else 1}'><b>{item['title']}</b><br>"
                    f"<span class='tag {item['conf']}'>{item['conflabel']}</span>{sent}<br>"
                    + "".join(f"<p class='sig'>• {s}</p>" for s in item["sigs"]) + "</div>",
                    unsafe_allow_html=True)
                if off:
                    if st.button("Thêm lại", key=f"add_{item['id']}"):
                        st.session_state.c_removed.discard(item["id"])
                        st.rerun()
                else:
                    c1, c2, _ = st.columns([0.30, 0.24, 0.46])
                    with c1:
                        if st.button("Đúng, tôi cần giúp chỗ này", key=f"yes_{item['id']}",
                                     use_container_width=True):
                            st.toast("Đã ghi nhận. Mục này được ưu tiên cao hơn cho giảng viên.")
                    with c2:
                        if st.button("Tôi ổn chỗ này — gỡ", key=f"rm_{item['id']}",
                                     use_container_width=True):
                            st.session_state.c_removed.add(item["id"])
                            st.toast("Đã gỡ khỏi danh sách. Giảng viên không còn thấy mục này.")
                            st.rerun()

        st.divider()
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Không gửi gì cho giảng viên phiên này", use_container_width=True):
                st.session_state.c_removed.update({"it1", "it2", "it3"})
                st.toast("Phiên này không có gì được gửi đi.")
                st.rerun()
        with c2:
            if st.button("Xem giảng viên đang nhìn thấy gì về tôi", type="primary",
                         use_container_width=True):
                st.session_state.c_step = 3
                st.rerun()

    # ---- state 3: phía giảng viên + quyền của user -----------------------
    else:
        st.markdown("#### Giảng viên đang nhìn thấy gì về bạn")
        st.caption("Thẻ này nằm trong danh sách hỗ trợ của buổi 12, xếp theo mức ưu tiên.")
        live = [i for i in ("it1", "it2", "it3") if i not in st.session_state.c_removed]
        gone = st.session_state.c_pulled or not live

        with st.container(border=True):
            prio = ("<span class='tag mute'>không còn trong danh sách</span>" if gone else
                    "<span class='tag stop'>Ưu tiên: CAO</span>" if len(live) >= 2 else
                    "<span class='tag warn'>Ưu tiên: TRUNG BÌNH</span>")
            st.markdown(f"**Học viên · lớp AI Foundation K7** &nbsp; {prio}<br>"
                        f"<span class='small'>Buổi 12 · cập nhật 22:05</span>",
                        unsafe_allow_html=True)
            if gone:
                st.caption("Bạn đã gỡ mình khỏi danh sách. Giảng viên không nhìn thấy gì "
                           "về phiên này.")
            else:
                rows = ["Chuẩn hoá L2 sau khi nhân tf × idf"]
                if "it2" in live:
                    rows.append("Định nghĩa tf, df và n")
                if "it3" in live:
                    rows.append("Chưa làm bài tập cuối slide 14")
                st.markdown("**Hệ thống cho rằng học viên này đang gặp khó ở:**<br>"
                            + "".join(f"<p class='sig'>• {r}</p>" for r in rows)
                            + "<br><span class='tag mute'>Gợi ý hành động: nhắn riêng cho "
                              "học viên này</span>", unsafe_allow_html=True)

        st.divider()
        st.markdown("#### Bạn muốn làm gì?")
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("Gỡ tôi khỏi danh sách này", use_container_width=True):
                st.session_state.c_pulled = True
                st.session_state.c_removed.update({"it1", "it2", "it3"})
                st.toast("Đã gỡ. Giảng viên không còn nhìn thấy bạn trong danh sách.")
                st.rerun()
        with c2:
            if st.button("Xoá dữ liệu hành vi phiên này", use_container_width=True):
                st.toast("Đã xoá dữ liệu hành vi của phiên xem lại này.")
        with c3:
            if st.button("Tắt hẳn tính năng này cho tôi", use_container_width=True):
                st.toast("Đã tắt. Từ phiên sau VLearn không tự tổng hợp nữa.")

        st.divider()
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("Đi tiếp slide 15", type="primary", use_container_width=True):
                st.toast("Bạn đã đi tiếp slide 15")
        with c2:
            if st.button("Quay lại danh sách", use_container_width=True):
                st.session_state.c_step = 2
                st.rerun()
        with c3:
            if st.button("Quay lại slide 14", use_container_width=True):
                st.session_state.c_step = 1
                st.rerun()


def _c_items(elapsed):
    """Ba mục digest của Option C.

    Tín hiệu đầu tiên của mục 1 là thời lượng phiên THẬT của tester (đo từ lúc mở
    option tới lúc bấm "Kết thúc phiên xem lại") — để tester phản ứng với một con số
    về chính mình. Các tín hiệu còn lại là fixture dựng sẵn, đánh dấu bằng comment;
    Streamlit không nhận được sự kiện hover nên không đo được dwell theo từng đoạn.
    KHÔNG suy ra số per-đoạn từ tổng thời gian — đó là bịa số, không phải đo.

    Mục 2 là false positive CÓ CHỦ Ý (rủi ro A2 của Day 17): tester phải tự phát hiện.
    Mục 3 là suy luận từ việc tester KHÔNG làm."""
    return [
        {"id": "it1", "title": "Chuẩn hoá L2 sau khi nhân tf × idf",
         "conf": "ok", "conflabel": "Độ tin cậy cao", "sent": True,
         "sigs": [f"Bạn ở lại slide 14 tổng cộng {fmt_secs(elapsed)}",   # ĐO THẬT
                  "Bạn quay lại đoạn này 2 lần",                          # fixture
                  "4 học viên khác trong lớp cũng dừng lâu ở đúng đoạn này"]},  # fixture
        {"id": "it2", "title": "Định nghĩa tf, df và n",
         "conf": "warn", "conflabel": "Độ tin cậy trung bình", "sent": False,
         "sigs": ["Bạn đọc đoạn này chậm hơn tốc độ trung bình của bạn",
                  "Bạn cuộn lên xem lại đoạn này sau khi đã đọc phần công thức"]},
        {"id": "it3", "title": "Bài tập cuối slide — vì sao \"+1\" khiến không trọng số nào bằng 0",
         "conf": "warn", "conflabel": "Độ tin cậy thấp", "sent": False,
         "sigs": ["Bạn chưa mở phần bài tập này",
                  "Bạn rời slide trước khi đọc tới cuối"]},               # fixture
    ]


# ================================================================ router ===
{"hub": screen_hub, "a": screen_a, "b": screen_b, "c": screen_c}[st.session_state.screen]()
