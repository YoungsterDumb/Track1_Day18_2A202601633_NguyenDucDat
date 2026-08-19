"""FastAPI entrypoint wiring both sections onto shared models."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from .config import CORS_ORIGINS
from .db import engine
from .routers import auth, course_long, in_class

app = FastAPI(title="Student Support Platform", version="1.0.0", description="In-class + course-long support, one API.")
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth.router)
app.include_router(in_class.router)
app.include_router(course_long.router)


@app.get("/health", tags=["ops"])
def health() -> dict[str, str]:
    """Liveness + database reachability, used by the compose health check."""
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
    return {"status": "ok", "database": "reachable"}
