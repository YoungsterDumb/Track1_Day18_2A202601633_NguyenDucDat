#!/usr/bin/env bash
set -euo pipefail

echo "waiting for database..."
python - <<'PY'
import time
import sqlalchemy
from app.config import DATABASE_URL

for attempt in range(60):
    try:
        sqlalchemy.create_engine(DATABASE_URL).connect().close()
        break
    except Exception as error:  # noqa: BLE001
        print(f"  db not ready ({attempt + 1}/60): {error.__class__.__name__}")
        time.sleep(2)
else:
    raise SystemExit("database never became reachable")
PY

alembic upgrade head

if [ "${SEED_ON_START:-true}" = "true" ]; then
  python -c "
from app.db import SessionLocal
from app.seed_data import seed_if_empty
session = SessionLocal()
print('seeded' if seed_if_empty(session) else 'seed skipped (data present)')
session.close()
"
fi

exec "$@"
