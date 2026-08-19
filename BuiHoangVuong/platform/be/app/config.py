"""Runtime configuration, all overridable through environment variables."""

import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg://ews:ews@db:5432/ews")
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
AUTH_SECRET = os.getenv("AUTH_SECRET", "dev-secret-change-me")
TOKEN_TTL_SECONDS = int(os.getenv("TOKEN_TTL_SECONDS", "28800"))
CORS_ORIGINS = [origin for origin in os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",") if origin]
SEED_ON_START = os.getenv("SEED_ON_START", "true").lower() == "true"
