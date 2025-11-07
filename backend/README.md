# FastAPI Backend

This directory contains the FastAPI application that powers the template backend. It ships with:

- Async SQLAlchemy models and Alembic migrations targeting PostgreSQL 17
- JWT-based authentication and refresh token rotation backed by Redis
- Redis integrations for caching and Celery background tasks
- OpenTelemetry hooks for metrics and tracing

## Quick Start

```bash
uv sync
uv run alembic upgrade head
uv run fastapi dev app/main.py
```

Environment variables live in `.env`. Copy `env.example` to `.env` before running the project.

## Key Commands

- `uv run pytest` – run the backend test suite
- `uv run alembic revision --autogenerate -m "message"` – create a new database migration
- `uv run celery -A app.infrastructure.messaging.tasks.celery_app worker --loglevel=info` – start background workers

See the repository root `README.md` for end-to-end instructions.

