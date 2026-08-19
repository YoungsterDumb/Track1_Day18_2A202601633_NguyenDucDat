"""Login and identity endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status

from ews_shared.security import check_password, issue_token

from ..config import AUTH_SECRET, TOKEN_TTL_SECONDS
from ..schemas import LoginRequest, TokenResponse
from ..security import current_user

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest) -> TokenResponse:
    """Exchange demo credentials for a signed bearer token."""
    if not check_password(payload.username, payload.password):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid username or password")
    username = payload.username.strip().lower()
    return TokenResponse(access_token=issue_token(username, AUTH_SECRET, TOKEN_TTL_SECONDS), username=username)


@router.get("/me")
def me(username: str = Depends(current_user)) -> dict[str, str]:
    """Return the caller identity behind the token."""
    return {"username": username}
