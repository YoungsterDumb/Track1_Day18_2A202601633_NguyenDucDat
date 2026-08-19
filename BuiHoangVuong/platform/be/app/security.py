"""Bearer-token dependency wrapping the shared demo auth."""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from ews_shared.security import verify_token

from .config import AUTH_SECRET

bearer = HTTPBearer(auto_error=False)


def current_user(credentials: HTTPAuthorizationCredentials | None = Depends(bearer)) -> str:
    """Return the authenticated username or raise 401."""
    token = credentials.credentials if credentials else None
    username = verify_token(token, AUTH_SECRET) if token else None
    if username is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid or expired token")
    return username
