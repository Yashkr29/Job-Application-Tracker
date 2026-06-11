# Backend

FastAPI backend for the Job Application Tracker.

## Commands

```bash
pip install -r requirements.txt
uvicorn app.main:app --host 127.0.0.1 --port 8051 --reload
pytest
ruff check app tests
alembic upgrade head
```

## API Groups

- `/api/auth`: registration, login, refresh, logout, password reset, email verification, profile management.
- `/api/applications`: CRUD, filters, CSV import/export, upcoming interviews, status updates, notes.
- `/api/tags`: tag CRUD and application tag links.
- `/api/contacts`: contact CRUD and linked applications.
- `/api/resumes`: PDF upload metadata and application resume links.
- `/api/stats`: overview, funnel, timeline, salary, sources.
- `/health`, `/health/db`, `/health/redis`: monitoring endpoints.

All JSON API responses use `{ success, data, message }`; errors use `{ success: false, error, details }`.
