"""Demo auth shared by API and tests: sha256 credentials + signed bearer tokens."""

from base64 import urlsafe_b64encode
from hashlib import sha256
from hmac import compare_digest, new as hmac_new
from time import time
from typing import Optional

USERS = {
    "teacher": sha256(b"teacher123").hexdigest(),
    "admin": sha256(b"admin123").hexdigest(),
}


def check_password(username: str, password: str) -> bool:
    """Return True when the username exists and the password hash matches."""
    expected = USERS.get(username.strip().lower())
    if expected is None:
        return False
    return compare_digest(expected, sha256(password.encode("utf-8")).hexdigest())


def issue_token(username: str, secret: str, ttl_seconds: int = 28800) -> str:
    """Return a signed `user.expiry.signature` bearer token."""
    payload = f"{username.strip().lower()}.{int(time()) + ttl_seconds}"
    signature = hmac_new(secret.encode(), payload.encode(), sha256).digest()
    return f"{payload}.{urlsafe_b64encode(signature).decode().rstrip('=')}"


def verify_token(token: str, secret: str) -> Optional[str]:
    """Return the username when the token is well-formed, unexpired, and correctly signed."""
    try:
        username, expiry, signature = token.split(".")
        payload = f"{username}.{expiry}"
        expected = urlsafe_b64encode(hmac_new(secret.encode(), payload.encode(), sha256).digest()).decode().rstrip("=")
    except (ValueError, AttributeError):
        return None
    if not compare_digest(expected, signature) or int(expiry) < time():
        return None
    return username
