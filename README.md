# Job Application Tracker

A staged full-stack job application tracker built from an empty repository.

## Stages

1. **Backend auth system**: FastAPI, async SQLAlchemy, JWT access/refresh tokens, refresh-token persistence, logout blacklist fallback, email verification token flow, password reset OTP, profile updates, account lockout, health checks.
2. **Applications CRUD**: job application pipeline, filtering, pagination, CSV import/export, status history, notes, tags, contacts, resumes, and analytics endpoints.
3. **React frontend**: React 18 + TypeScript + Vite, Tailwind CSS variables, Zustand auth store, TanStack Query, React Hook Form + Zod auth pages, protected routes, list/Kanban applications view, dashboard, stats charts, contacts, resumes, settings.

## Local Backend

```bash
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --host 127.0.0.1 --port 8051 --reload
```

The backend defaults to local SQLite for development. Set `DATABASE_URL` to your Supabase PostgreSQL async connection string for production.

## Local Frontend

```bash
cd frontend
npm install
copy .env.example .env
npm run dev -- --host=127.0.0.1 --port=5173
```

## Tests

```bash
cd backend
pytest
```

## Deployment Notes

- Backend is ready for Render via `backend/Dockerfile`.
- Frontend is ready for Vercel via Vite build output.
- Supabase Storage and SMTP adapters are represented behind services and configured through environment variables.
- Redis uses a local in-memory fallback for development/tests; set `REDIS_URL` or Upstash vars in production.
