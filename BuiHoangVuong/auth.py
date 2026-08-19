"""Minimal session-based auth for the dashboard (demo accounts, no user table)."""

from hashlib import sha256
from hmac import compare_digest

import streamlit as st

# Demo accounts only: username -> sha256(password). Replace before any real deployment.
USERS = {
    "teacher": sha256(b"teacher123").hexdigest(),
    "admin": sha256(b"admin123").hexdigest(),
}

SESSION_KEYS = ("logged_in", "username", "ranking", "synced")


def check_password(username: str, password: str) -> bool:
    """Return True when the username exists and the password hash matches."""
    expected = USERS.get(username.strip().lower())
    if expected is None:
        return False
    return compare_digest(expected, sha256(password.encode("utf-8")).hexdigest())


def is_logged_in() -> bool:
    """Return True when the current Streamlit session is authenticated."""
    return bool(st.session_state.get("logged_in"))


def login(username: str) -> None:
    """Mark the session as authenticated for the given user."""
    st.session_state["logged_in"] = True
    st.session_state["username"] = username.strip().lower()


def logout() -> None:
    """Clear every session key owned by the app."""
    for key in SESSION_KEYS:
        st.session_state.pop(key, None)
