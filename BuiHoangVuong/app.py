"""Streamlit dashboard for the student early warning prototype."""

from pathlib import Path
from html import escape

import pandas as pd
import streamlit as st

import auth
from explain import explain
from scoring import get_ranking
from sync import sync_school_data

DB_PATH = Path(__file__).with_name("students.db")


def color_risk(value: object) -> str:
    """Return a background color for a risk category or numeric score."""
    text = str(value)
    if "High" in text or (text.isdigit() and int(text) >= 70):
        return "background-color: #ffc7ce; color: #9c0006"
    if "Medium" in text or (text.isdigit() and int(text) >= 40):
        return "background-color: #ffeb9c; color: #9c6500"
    return "background-color: #c6efce; color: #006100"


st.set_page_config(page_title="Student Early Warning System", page_icon="🎯", layout="wide")

# Design Tokens + CSS Injection. Keep this inline so the dashboard remains portable.
st.markdown(
    """
<style>
:root {
  --ink: #0B0B0F;
  --panel: #131318;
  --panel-soft: #19191f;
  --line: rgba(255,255,255,.10);
  --muted: #96969f;
  --text: #f6f4ee;
  --gold: #D4AF37;
  --gold-light: #f1d579;
  --green: #8fd6ad;
  --amber: #e8c978;
  --red: #ee9999;
  --space-1: .45rem;
  --space-2: .8rem;
  --space-3: 1.25rem;
  --space-4: 2rem;
  --space-5: 3.5rem;
  --radius: 14px;
  --display: Georgia, 'Times New Roman', serif;
  --body: Inter, ui-sans-serif, system-ui, -apple-system, sans-serif;
}
html, body, [data-testid="stAppViewContainer"] { background: var(--ink); }
[data-testid="stHeader"] { background: transparent; }
[data-testid="stAppViewContainer"] > .main { background: radial-gradient(circle at 85% 0%, rgba(212,175,55,.08), transparent 28rem); }
.block-container { max-width: 1400px; padding: 3rem 4rem 5rem; }
* { font-family: var(--body); }
h1, h2, h3, [data-testid="stMetricValue"] { font-family: var(--display) !important; color: var(--text) !important; letter-spacing: -.035em; }
h1 { font-size: clamp(2.8rem, 6vw, 5.8rem) !important; line-height: .98 !important; }
h2 { font-size: clamp(2rem, 4vw, 3.2rem) !important; }
h3 { font-size: 1.35rem !important; letter-spacing: -.01em; }
p, label, [data-testid="stCaptionContainer"] { color: var(--muted) !important; }
.eyebrow, .login-kicker { color: var(--gold-light) !important; font-size: .72rem; font-weight: 800; letter-spacing: .2em; text-transform: uppercase; }
.login-hero { min-height: 40vh; display: flex; flex-direction: column; justify-content: center; padding: 4rem 0 2rem; }
.login-hero h1 { max-width: 780px; margin: .6rem 0 1rem; }
.login-hero p { max-width: 520px; font-size: 1.05rem; line-height: 1.7; }
.login-note { border-left: 2px solid var(--gold); padding-left: 1rem; margin-top: 2rem; font-size: .82rem; }
[data-testid="stForm"] { background: rgba(25,25,31,.82); border: 1px solid var(--line); border-radius: 20px; padding: 2rem; box-shadow: 0 24px 80px rgba(0,0,0,.35); backdrop-filter: blur(18px); }
[data-testid="stTextInput"] input { background: rgba(255,255,255,.05); color: var(--text); border: 1px solid var(--line); border-radius: 9px; }
[data-testid="stTextInput"] input:focus { border-color: var(--gold); box-shadow: 0 0 0 1px var(--gold); }
button[kind="primary"], [data-testid="stFormSubmitButton"] button { background: linear-gradient(110deg, #c49b22, var(--gold-light)); color: #16130b !important; border: 0; font-weight: 800; border-radius: 8px; transition: transform .2s, box-shadow .2s; }
button[kind="primary"]:hover, [data-testid="stFormSubmitButton"] button:hover { transform: translateY(-2px); box-shadow: 0 10px 24px rgba(212,175,55,.22); }
button { border-radius: 8px !important; transition: transform .2s, border-color .2s, background .2s !important; }
button:hover { transform: translateY(-1px); border-color: var(--gold) !important; }
[data-testid="stSidebar"] { background: #0e0e12; border-right: 1px solid var(--line); }
[data-testid="stSidebar"] > div:first-child { padding: 2rem 1.25rem; }
.profile-card { padding: 1.2rem; margin: 1rem 0 1.5rem; border: 1px solid var(--line); border-radius: var(--radius); background: linear-gradient(145deg, rgba(212,175,55,.13), rgba(255,255,255,.025)); }
.profile-mark { width: 42px; height: 42px; display: grid; place-items: center; border-radius: 50%; color: #201a09; background: var(--gold); font-weight: 900; margin-bottom: 1rem; }
.profile-name { color: var(--text); font-weight: 800; }
.profile-role { color: var(--muted); font-size: .76rem; margin-top: .2rem; }
.dashboard-head { padding: 1.5rem 0 2.5rem; }
.dashboard-head h1 { max-width: 860px; margin: .5rem 0 1rem; }
.dashboard-head p { max-width: 620px; font-size: 1rem; line-height: 1.65; }
.section-label { color: var(--gold-light); font-size: .72rem; font-weight: 800; letter-spacing: .17em; text-transform: uppercase; margin: 2.5rem 0 1rem; }
.metric-card { min-height: 112px; padding: 1.1rem 1.25rem; border: 1px solid var(--line); border-radius: var(--radius); background: var(--panel); }
.metric-card .metric-value { color: var(--text); font-family: var(--display); font-size: 2.35rem; line-height: 1; }
.metric-card .metric-label { color: var(--muted); font-size: .75rem; margin-top: .7rem; }
.metric-card.high { border-top: 2px solid var(--red); }
.metric-card.medium { border-top: 2px solid var(--amber); }
.metric-card.low { border-top: 2px solid var(--green); }
.ranking-card { height: 100%; padding: 1.25rem; border: 1px solid var(--line); border-radius: var(--radius); background: linear-gradient(150deg, var(--panel-soft), var(--panel)); transition: transform .25s, border-color .25s, box-shadow .25s; }
.ranking-card:hover { transform: translateY(-4px); border-color: rgba(212,175,55,.65); box-shadow: 0 18px 40px rgba(0,0,0,.25); }
.card-top { display: flex; align-items: center; justify-content: space-between; gap: .5rem; }
.card-rank { color: var(--gold); font-family: var(--display); font-size: 1.2rem; }
.risk-pill { padding: .3rem .55rem; border-radius: 999px; font-size: .65rem; font-weight: 800; letter-spacing: .08em; text-transform: uppercase; }
.risk-pill.high { color: var(--red); background: rgba(238,153,153,.12); }
.risk-pill.medium { color: var(--amber); background: rgba(232,201,120,.12); }
.risk-pill.low { color: var(--green); background: rgba(143,214,173,.12); }
.student-name { color: var(--text); font-size: 1.12rem; font-weight: 750; margin: 1.1rem 0 .15rem; }
.student-id { color: var(--muted); font-size: .74rem; }
.score-line { display: flex; align-items: baseline; gap: .35rem; margin-top: 1.2rem; }
.score-number { color: var(--gold-light); font-family: var(--display); font-size: 2rem; }
.score-caption { color: var(--muted); font-size: .72rem; }
.card-details { display: grid; grid-template-columns: 1fr 1fr; gap: .7rem; margin-top: 1rem; padding-top: 1rem; border-top: 1px solid var(--line); }
.detail-label { color: var(--muted); display: block; font-size: .66rem; text-transform: uppercase; letter-spacing: .06em; }
.detail-value { color: var(--text); display: block; font-size: .86rem; margin-top: .2rem; }
[data-testid="stExpander"] { border: 1px solid var(--line); border-radius: var(--radius); background: var(--panel); margin-bottom: .65rem; transition: border-color .2s, background .2s; }
[data-testid="stExpander"]:hover { border-color: rgba(212,175,55,.55); background: var(--panel-soft); }
[data-testid="stExpander"] summary p { color: var(--text) !important; font-size: .88rem; font-weight: 650; }
[data-testid="stRadio"] label { color: var(--muted) !important; }
[data-testid="stDownloadButton"] button { width: 100%; }
[data-testid="stAlert"] { border-radius: 10px; border: 1px solid var(--line); }
@media (max-width: 800px) { .block-container { padding: 2rem 1.1rem 3rem; } .login-hero { min-height: 34vh; padding-top: 2rem; } .dashboard-head { padding-top: .5rem; } }
/* Login surface: intentionally separate from the dark dashboard theme. */
body:has(.login-page), body:has(.login-page) [data-testid="stAppViewContainer"], body:has(.login-page) [data-testid="stAppViewContainer"] > .main { background: #fbfaf8 !important; }
body:has(.login-page) [data-testid="stHeader"] { background: #fbfaf8 !important; }
body:has(.login-page) .block-container { max-width: 100%; min-height: 100vh; padding: 0 1.25rem 2rem; }
.login-page { width: 100%; max-width: 400px; margin: 0 auto; padding: 10vh 0 2rem; color: #172033; }
.login-brand { display: flex; align-items: center; gap: .6rem; color: #172033; font-size: .9rem; font-weight: 700; letter-spacing: -.01em; }
.login-brand-mark { display: grid; place-items: center; width: 28px; height: 28px; border-radius: 8px; background: #253b73; color: #fff; font-size: .78rem; font-weight: 800; }
.login-copy { margin: 3.25rem 0 1.75rem; }
.login-copy h1 { color: #172033 !important; font-family: var(--body) !important; font-size: 2rem !important; font-weight: 700; letter-spacing: -.045em; line-height: 1.12 !important; margin: 0 0 .7rem; }
.login-copy p { color: #667085 !important; font-size: .95rem; line-height: 1.55; margin: 0; }
body:has(.login-page) [data-testid="stVerticalBlock"] > [data-testid="stElementContainer"] { color: #172033; }
body:has(.login-page) [data-testid="stButton"] button, body:has(.login-page) [data-testid="stFormSubmitButton"] button { min-height: 44px; border: 1px solid #d8dce5; border-radius: 10px !important; background: #fff; color: #344054 !important; font-family: var(--body); font-size: .9rem; font-weight: 600; box-shadow: 0 1px 2px rgba(16,24,40,.04); }
body:has(.login-page) [data-testid="stButton"] button:hover, body:has(.login-page) [data-testid="stFormSubmitButton"] button:hover { border-color: #253b73 !important; background: #f8f9fc; transform: none; box-shadow: 0 2px 5px rgba(16,24,40,.08); }
body:has(.login-page) [data-testid="stButton"] button:focus-visible, body:has(.login-page) [data-testid="stFormSubmitButton"] button:focus-visible { outline: 3px solid rgba(37,59,115,.2); outline-offset: 2px; }
body:has(.login-page) [data-testid="stButton"] button:disabled { color: #344054 !important; opacity: 1; cursor: not-allowed; }
body:has(.login-page) [data-testid="stForm"] { margin-top: .75rem; padding: 0; border: 0; border-radius: 0; background: transparent; box-shadow: none; backdrop-filter: none; }
.login-divider { display: flex; align-items: center; gap: .75rem; margin: 1.25rem 0; color: #98a2b3; font-size: .78rem; }
.login-divider::before, .login-divider::after { content: ""; height: 1px; flex: 1; background: #e4e7ec; }
body:has(.login-page) [data-testid="stTextInput"] { margin-bottom: .85rem; }
body:has(.login-page) [data-testid="stTextInput"] label { color: #344054 !important; font-size: .8rem; font-weight: 600; margin-bottom: .35rem; }
body:has(.login-page) [data-testid="stTextInput"] input { min-height: 44px; box-sizing: border-box; background: #fff; color: #172033; border: 1px solid #d0d5dd; border-radius: 10px; font-size: .9rem; }
body:has(.login-page) [data-testid="stTextInput"] input::placeholder { color: #98a2b3; }
body:has(.login-page) [data-testid="stTextInput"] input:focus { border-color: #253b73; box-shadow: 0 0 0 3px rgba(37,59,115,.12); }
.password-tools { display: flex; justify-content: flex-end; margin: -.3rem 0 .85rem; }
body:has(.login-page) [data-testid="stFormSubmitButton"] button:not([kind="primary"]) { min-height: auto; padding: 0 .15rem; border: 0; background: transparent; color: #536aa1 !important; box-shadow: none; font-size: .75rem; }
body:has(.login-page) [data-testid="stFormSubmitButton"] button:not([kind="primary"]):hover { background: transparent; color: #253b73 !important; text-decoration: underline; }
body:has(.login-page) [data-testid="stFormSubmitButton"] button[kind="primary"] { width: 100%; margin-top: .25rem; border-color: #253b73; background: #253b73; color: #fff !important; font-weight: 700; }
body:has(.login-page) [data-testid="stFormSubmitButton"] button[kind="primary"]:hover { background: #1d2f5d; border-color: #1d2f5d !important; box-shadow: 0 4px 10px rgba(37,59,115,.18); }
.forgot-row { display: flex; justify-content: flex-end; margin-top: .5rem; }
.forgot-link { color: #536aa1 !important; font-size: .78rem; text-decoration: none; }
.forgot-link:hover { color: #253b73 !important; text-decoration: underline; }
.login-footer { margin-top: 4rem; color: #98a2b3 !important; font-size: .75rem; text-align: center; }
body:has(.login-page) [data-testid="stAlert"] { margin-top: .8rem; border: 1px solid #f1b8b8; border-radius: 10px; background: #fff5f5; color: #b42318; }
@media (max-width: 520px) { .login-page { padding-top: 2.5rem; } .login-copy { margin-top: 2.5rem; } .login-footer { margin-top: 3rem; } }
</style>
""",
    unsafe_allow_html=True,
)

if not auth.is_logged_in():
    show_password = st.session_state.get("show_password", False)
    st.markdown(
        """
        <div class="login-page">
          <div class="login-brand"><span class="login-brand-mark">S</span><span>Student Success</span></div>
          <div class="login-copy">
            <h1>Chào mừng trở lại</h1>
            <p>Đăng nhập để tiếp tục hỗ trợ học viên.</p>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    form_left, form_center, form_right = st.columns([1, 1.05, 1])
    with form_center:
        st.button("G  Tiếp tục với Google", key="google_sso", use_container_width=True, disabled=True, help="Google SSO chưa được cấu hình cho workspace này.")
        st.markdown('<div class="login-divider"><span>hoặc</span></div>', unsafe_allow_html=True)
        with st.form("login"):
            username = st.text_input("Email", key="login_email", placeholder="ten@truong.edu.vn", autocomplete="username")
            password_col, toggle_col = st.columns([5, 1])
            with password_col:
                password = st.text_input("Mật khẩu", key="login_password", type="default" if show_password else "password", placeholder="Nhập mật khẩu", autocomplete="current-password")
            with toggle_col:
                st.markdown('<div style="height: 1.7rem"></div>', unsafe_allow_html=True)
                toggle_password = st.form_submit_button("Ẩn" if show_password else "Hiện", use_container_width=True)
            login_submitted = st.form_submit_button("Đăng nhập", use_container_width=True, type="primary")
        st.markdown('<div class="forgot-row"><a class="forgot-link" href="#access-help">Quên mật khẩu?</a></div>', unsafe_allow_html=True)
        if toggle_password:
            st.session_state["show_password"] = not show_password
            st.rerun()
        if login_submitted:
            with st.spinner("Đang đăng nhập…"):
                if auth.check_password(username, password):
                    auth.login(username)
                    st.rerun()
                else:
                    st.error("Email hoặc mật khẩu không đúng. Vui lòng thử lại.")
        st.markdown('<div class="login-footer" id="access-help">Cần quyền truy cập? Liên hệ quản trị viên.</div>', unsafe_allow_html=True)
    st.stop()

with st.sidebar:
    username = escape(str(st.session_state["username"]))
    st.markdown(
        f'<div class="eyebrow">Early warning system</div><div class="profile-card">'
        f'<div class="profile-mark">{username[:1].upper()}</div>'
        f'<div class="profile-name">{username}</div><div class="profile-role">Academic support workspace</div></div>',
        unsafe_allow_html=True,
    )
    if st.button("Sign out", use_container_width=True):
        auth.logout()
        st.rerun()

st.markdown(
    """
    <div class="dashboard-head">
      <div class="eyebrow">Student success intelligence · 2026</div>
      <h1>Make the next<br>conversation count.</h1>
      <p>A local, rule-based view of attendance, assessment momentum, and the students who may need timely support.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

sync_col, score_col = st.columns(2)
with sync_col:
    if st.button("Sync school data  →", use_container_width=True, type="primary"):
        mix = sync_school_data(DB_PATH)
        st.session_state["ranking"] = get_ranking(DB_PATH)
        st.success(f"Synced 50 students ({mix['high']} high / {mix['mid']} mid / {mix['low']} low risk profiles).")
with score_col:
    if st.button("Recalculate risk scores", use_container_width=True):
        try:
            ranking = get_ranking(DB_PATH)
            if ranking.empty:
                st.warning("The database is empty. Sync school data first.")
            else:
                st.session_state["ranking"] = ranking
        except (OSError, ValueError, RuntimeError) as error:
            st.error(f"Could not calculate scores: {error}")

ranking = st.session_state.get("ranking", pd.DataFrame())
if ranking.empty:
    st.markdown('<div class="section-label">Your first move</div>', unsafe_allow_html=True)
    st.info("Use **Sync school data** to pull the roster and calculate the ranking.")
else:
    high = int((ranking["risk_score"] >= 70).sum())
    medium = int(((ranking["risk_score"] >= 40) & (ranking["risk_score"] < 70)).sum())
    low = int((ranking["risk_score"] < 40).sum())
    metric_cols = st.columns(3)
    metric_data = [("high", "High risk", high, "70+ score"), ("medium", "Medium risk", medium, "40–69 score"), ("low", "Low risk", low, "Under 40 score")]
    for column, (tone, label, value, hint) in zip(metric_cols, metric_data):
        with column:
            st.markdown(f'<div class="metric-card {tone}"><div class="metric-value">{value}</div><div class="metric-label">{label} · {hint}</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="section-label">Live ranking · students needing attention</div>', unsafe_allow_html=True)
    card_cols = st.columns(3)
    for position, (_, row) in enumerate(ranking.iterrows()):
        tone = str(row["risk_category"]).split()[0].lower()
        rank = int(ranking.index[ranking["student_id"] == row["student_id"]][0]) + 1
        card = (
            f'<div class="ranking-card"><div class="card-top"><span class="card-rank">#{rank:02d}</span>'
            f'<span class="risk-pill {tone}">{escape(str(row["risk_category"]))}</span></div>'
            f'<div class="student-name">{escape(str(row["name"]))}</div><div class="student-id">ID {escape(str(row["student_id"]))}</div>'
            f'<div class="score-line"><span class="score-number">{row["risk_score"]}</span><span class="score-caption">/ 100 risk score</span></div>'
            f'<div class="card-details"><div><span class="detail-label">Average</span><span class="detail-value">{row["avg_score"]}/10</span></div>'
            f'<div><span class="detail-label">Trend</span><span class="detail-value">{float(row["score_trend"]):+.2f}</span></div>'
            f'<div><span class="detail-label">Failed</span><span class="detail-value">{row["failed_count"]} assessments</span></div>'
            f'<div><span class="detail-label">Logins</span><span class="detail-value">{row["logins_7d"]} in 7 days</span></div></div></div>'
        )
        with card_cols[position % 3]:
            st.markdown(card, unsafe_allow_html=True)

    st.download_button("Download complete ranking · CSV", ranking.to_csv(index=False).encode("utf-8"), "student_risk_ranking.csv", "text/csv")

    st.markdown('<div class="section-label">Why this rank?</div>', unsafe_allow_html=True)
    category = st.radio("Filter", ["All", "High Risk", "Medium Risk", "Low Risk"], horizontal=True)
    shown = ranking if category == "All" else ranking[ranking["risk_category"] == category]
    limit = st.slider("Students to explain", 1, max(len(shown), 1), min(10, max(len(shown), 1)))
    for _, row in shown.head(limit).iterrows():
        rank = int(ranking.index[ranking["student_id"] == row["student_id"]][0]) + 1
        with st.expander(f"#{rank} · {row['name']} — {row['risk_category']} ({row['risk_score']}/100)"):
            st.write(f"Average score: {row['avg_score']}/10 | Trend: {row['score_trend']:+.2f} per assessment")
            st.write(f"Failed assessments: {row['failed_count']} | Logins in last 7 days: {row['logins_7d']}")
            st.info(explain(row.to_dict(), rank))
