# FastAPI + Vue Template

Full-stack starter that pairs a FastAPI 0.115 backend with a Vue 3.5 SPA, PostgreSQL 17, Redis 7.4, and containerized tooling. It includes JWT authentication (with refresh tokens), Alembic migrations, Celery workers, and ready-to-extend Docker Compose orchestration.

## Features

- **Backend** (`backend/`)
  - FastAPI with async SQLAlchemy 2.0 models and Alembic migrations
  - JWT access + refresh tokens stored in PostgreSQL/Redis
  - Redis-integrated caching and Celery background worker scaffold
  - Structured logging via `structlog` and OpenTelemetry hooks

- **Frontend** (`frontend/`)
  - Vue 3 + Vite 6 + TypeScript + Pinia 3 + Vue Router 5
  - Auth flows (register/login/logout) wired to the backend API
  - UnoCSS utility styling and Vitest/Playwright testing scaffolds

- **Infrastructure**
  - Docker Compose stack with backend, frontend, PostgreSQL, Redis, Celery worker, and Mailpit
  - Postgres init scripts & Nginx reverse proxy template for production
  - `Makefile` with common workflows (`dev`, `lint`, `test`, `migrate`)

## Prerequisites

- Python 3.13+
- Node.js 22 (pnpm recommended)
- Docker Engine 27 with Compose V2
- `uv` (https://docs.astral.sh/uv/) and `pnpm` are suggested for local development

## Getting Started

```bash
# 1. Copy environment templates
cp backend/env.example backend/.env
cp frontend/.env.example frontend/.env

# 2. Start the stack
docker compose up --build

# 3. Apply initial migrations (in another terminal)
cd backend
uv run alembic upgrade head

# 4. Visit apps
# Backend docs: http://localhost:8000/docs
# Frontend SPA: http://localhost:5173
```

### Local (non-Docker) development

```bash
# Backend
cd backend
uv sync
uv run alembic upgrade head
uv run fastapi dev app/main.py

# Frontend
cd ../frontend
pnpm install
pnpm dev
```

### Lint & Test

```bash
make lint
make test
```

## Project Layout

Key directories:

- `backend/app`: FastAPI application (routers, services, domain models, infra adapters)
- `backend/alembic`: Migration environment + versioned scripts
- `frontend/src`: Vue SPA (router, stores, components, UnoCSS theme)
- `infrastructure/`: Docker, Nginx, and deployment scaffolding
- `docs/`: Architectural notes and proposal

## Next Steps

- Configure CI/CD (see `.github/workflows` scaffold placeholder)
- Integrate your chosen secret manager for production credentials
- Extend the domain models, services, and Vue routes to suit your product
- Hook up observability targets (Prometheus, Grafana, Sentry) via the provided OpenTelemetry entry points

See `docs/fastapi-vue-template-proposal.md` for the rationale behind the stack and structure.
