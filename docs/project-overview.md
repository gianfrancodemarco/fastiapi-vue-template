# FastAPI + Vue Template Reference

Structured documentation for onboarding and extending the FastAPI + Vue starter. Content is organized by domain: General repository context, Backend internals, and Frontend architecture.

---

## General

### Purpose & Scope
- Deliver a secure, batteries-included starter that pairs a FastAPI backend with a Vue 3 SPA.
- Provide out-of-the-box authentication, background jobs, linting/testing pipelines, and Docker-based infrastructure.

### Repository Layout

```
fastiapi-vue-template/
├─ backend/                  # FastAPI application and Python tooling
├─ frontend/                 # Vue 3 SPA and TypeScript tooling
├─ docs/                     # Project documentation & ADRs
├─ infrastructure/           # Shared infra assets (e.g., Postgres init SQL)
├─ docker-compose.yml        # Local orchestration of app + services
├─ Makefile                  # Cross-stack developer commands
├─ README.md                 # Repository-level quick start
└─ CONTRIBUTING.md           # Contribution guidelines
```

### Languages, Runtimes, Tooling
- **Languages**: `Python 3.13`, `TypeScript 5`, `Vue 3` single-file components.
- **Package Management**: `uv` for Python (`pyproject.toml`, `uv.lock`), `pnpm 9` for Node/TypeScript (`package.json`).
- **Containerization**: `Docker` + `docker-compose.yml` orchestrate FastAPI, Vite, PostgreSQL 17, and Redis 5.
- **Developer Utilities**: `Makefile` exposes lint/test/build commands; VS Code tasks/launch configs ship under `.vscode/`.

### Quality, Observability, Extension Points
- **Linters/Formatters**: `ruff`, `mypy`, `eslint`, `prettier` enforce code quality across stacks.
- **Testing Stack**: `pytest` + `pytest-asyncio` (backend), `vitest`, `@vue/test-utils`, `playwright` (frontend).
- **Telemetry**: `structlog` for structured logging, optional `opentelemetry-sdk` + OTLP exporter via `OTLP_ENDPOINT`.
- **Shared Extension Hooks**: Architecture Decision Records live in `docs/architecture-decision-records/`; infrastructure SQL seeded under `infrastructure/docker/`.

### Cross-Cutting Concerns
- **Authentication Lifecycle**: Backend issues JWT access + refresh tokens, caches identifiers in Redis, and persists refresh tokens in PostgreSQL; frontend handles token storage/refresh via Axios interceptors and Pinia store coordination.
- **Background Processing**: Celery worker integrates with Redis broker/result backend; extend by adding tasks to `app.infrastructure.messaging.tasks`.
- **Deployment Readiness**: Backend and frontend each expose Dockerfiles; Compose file models local topology and can inform production manifests.

### Shared Commands
- `docker compose up --build` – boot local stack (API, SPA, PostgreSQL, Redis).
- `make lint`, `make test` – run aggregated quality gates if configured.
- `uv sync`, `pnpm install` – install backend/frontend dependencies respectively.

---

## Backend

### Folder Structure

```
backend/
├─ app/
│  ├─ api/                   # FastAPI routers, dependencies, versioned endpoints
│  ├─ core/                  # Settings, logging, security helpers
│  ├─ domain/models/         # SQLAlchemy ORM entities (User, RefreshToken)
│  ├─ infrastructure/        # DB sessions, repositories, cache, messaging
│  ├─ schemas/               # Pydantic request/response contracts
│  ├─ services/              # Domain logic (auth, users)
│  ├─ tests/                 # Pytest suites (API, services, integration)
│  └─ main.py                # FastAPI app factory + lifespan hooks
├─ alembic/                  # Migration environment and versioned scripts
├─ pyproject.toml            # Project metadata, dependencies, tooling config
├─ uv.lock                   # Resolved dependency versions for reproducibility
├─ Dockerfile                # Backend container image definition
└─ env.example               # Sample environment configuration
```

### Tech Stack & Services
- **FastAPI** for async HTTP handling, automatic OpenAPI, and dependency injection.
- **SQLAlchemy 2 (async)** targeting **PostgreSQL 17** for persistence.
- **Alembic** for schema migrations and version control.
- **Redis 5** for token caching and Celery broker/result storage.
- **Celery 5** orchestrating background tasks (`app.infrastructure.messaging.tasks`).
- **Auth Components**: `PyJWT`, `passlib[bcrypt]`, `bcrypt` for JWT issuance and password hashing.
- **Observability**: `structlog`, `opentelemetry-sdk`, `httpx` for future integrations.

### Configuration & Lifespan
- `app/core/config.py`: Loads environment via `pydantic-settings`, exposes nested config (CORS, JWT, Celery, DB URIs) and computed DSNs (`database_uri`, `sync_database_uri`).
- `app/main.py`: Builds FastAPI app, sets CORS via `settings.cors`, verifies DB connectivity on startup, and disposes engine/Redis client on shutdown.
- `.env` derived from `env.example` supplies secrets, connection strings, and toggles (`debug`, `environment`).

### API & Service Layers
- `app/api/router.py` mounts `/api/v1`; `v1/routes.py` registers routers for `health`, `auth`, and `users` endpoints.
- `app/api/deps.py`: Shared dependency providers (DB session, Redis client, `get_current_user`).
- `app/api/v1/endpoints/auth.py`: Implements `/register`, `/login`, `/refresh`, `/logout`; maps domain errors to HTTP statuses.
- `app/api/v1/endpoints/users.py`: Provides `/users/me` (current user) and `/users/` listings with authentication guard.
- `app/services/users.py`: Handles registration (duplicate email checks, password hashing), authentication (`last_login_at` updates), retrieval, listing.
- `app/services/auth.py`: Issues tokens, persists refresh tokens, manages Redis caches, and enforces single-use refresh semantics.

### Persistence, Infrastructure, Background Jobs
- `app/domain/models/user.py` & `refresh_token.py`: SQLAlchemy models inheriting `TimestampMixin` from `infrastructure/db/base.py` for automatic timestamps.
- `app/infrastructure/db/session.py`: Creates global async engine (`create_async_engine`) and session factory (`SessionLocal`).
- `app/infrastructure/db/repositories/users.py`: Encapsulates queries for users/refresh tokens, revocation, and activity checks.
- `app/infrastructure/cache/redis.py`: Provides cached Redis client lifecycle, including shutdown cleanup.
- `app/infrastructure/messaging/tasks.py`: Configures Celery app, queues, and includes sample `heartbeat` task.
- `alembic/versions/`: Stores migration scripts (e.g., `create_users_and_tokens.py`) aligning DB schema.

### Security & Auth Flow
- `app/core/security.py`: Utility functions for creating/decoding tokens, verifying token type, extracting subject/JTI, password hashing/verification.
- `app/api/deps.get_current_user`: Validates bearer tokens, ensures access token type, checks Redis for active token IDs, fetches `User` entity, returns `UserRead` schema.
- `services/auth.logout`: Revokes refresh tokens in DB to prevent replay; refresh flow rotates tokens by revoking old IDs before issuing new ones.

### Testing & Developer Commands
- Tests located in `app/tests/` (example: `tests/api/test_health.py`).
- `pyproject.toml` configures `pytest` (`asyncio_mode=auto`), coverage, `ruff`, and strict `mypy` settings.
- Common commands:
  - `uv sync` – install dependencies.
  - `uv run fastapi dev app/main.py` – start dev server with auto reload.
  - `uv run alembic upgrade head` – apply migrations.
  - `uv run pytest` – execute test suite.
  - `uv run celery -A app.infrastructure.messaging.tasks.celery_app worker --loglevel=info` – start background worker.

---

## Frontend

### Folder Structure

```
frontend/
├─ src/
│  ├─ api/                   # Axios client, token storage, API helpers
│  ├─ components/            # Reusable presentation components
│  ├─ composables/           # Domain-specific Vue composables (future expansion)
│  ├─ layouts/               # Shared layout shells
│  ├─ router/                # Route definitions & guards
│  ├─ stores/                # Pinia stores (auth and future domains)
│  ├─ styles/                # UnoCSS configuration helpers
│  └─ views/                 # Routed pages (Auth, Dashboard, Settings)
├─ public/                   # Static assets (served as-is)
├─ tests/                    # Vitest unit suites & Playwright e2e setup
├─ package.json              # Metadata, scripts, dependency manifest
├─ vite.config.ts            # Vite dev/build configuration
├─ uno.config.ts             # UnoCSS presets and theme tokens
└─ Dockerfile                # Frontend container image definition
```

### Tech Stack & Libraries
- **Core**: `Vue 3` with `<script setup>` syntax and composition API, `TypeScript 5` for static typing.
- **Tooling**: `Vite 6` dev server/build, `pnpm` package manager.
- **State & Data**: `Pinia 3` for app state, `@tanstack/vue-query 5` for server-state caching.
- **Networking**: `Axios 1.7` for REST integration with configured interceptors.
- **Routing**: `Vue Router 4` with history mode and navigation guards.
- **Styling**: `UnoCSS 0.60` with presets for utility classes, resets, iconography.
- **Validation**: `zod` available for runtime schema validation (future use in composables/forms).

### Configuration & Environment
- `vite.config.ts`: Registers Vue + UnoCSS plugins, defines alias `@ → src`, configures dev (`5173`) and preview (`4173`) ports.
- `.env` (optional): Configure `VITE_API_BASE_URL`; code defaults to `http://localhost:8000/api`.
- `uno.config.ts`: Customize utility presets, tokens, and shortcuts for design system needs.

### Application Bootstrap & State Management
- `src/main.ts`: Creates Vue app, installs Pinia, Vue Query, router, and global UnoCSS resets (`@unocss/reset/tailwind.css`, `uno.css`).
- `App.vue`: Root shell ready for navigation/layout composition; triggers auth store initialization to hydrate user state on launch.
- `src/api/token-storage.ts`: Wraps `localStorage` for access/refresh tokens with publish/subscribe notifications.
- `src/stores/auth.ts`: Central auth store maintaining user profile, token snapshots, loading/error states, and actions (`login`, `register`, `logout`, `loadUserProfile`, `initialize`).

### Routing & Views
- `src/router/index.ts`: Defines routes with metadata flags (`requiresAuth`, `guestOnly`) and global `beforeEach` guard leveraging auth store for redirects.
- `src/views/`:
  - `Auth/LoginView.vue`, `Auth/RegisterView.vue` – Authentication forms leveraging auth store actions.
  - `DashboardView.vue` – Protected landing page highlighting environment info and next steps.
  - `SettingsView.vue` – Scaffold for future account/preferences UI.
- `src/layouts/` & `src/components/`: Intended for shared UI wrappers and reusable presentation components.

### HTTP Client & Auth Flow
- `src/api/http.ts`:
  - Axios instance with base URL derived from `VITE_API_BASE_URL` (trailing slash stripped).
  - Request interceptor injects bearer access token when present.
  - Response interceptor handles `401` responses by invoking `/auth/refresh`, queues concurrent refresh calls, updates tokens, and retries original requests.
- Interacts directly with backend `/auth` endpoints and respects Redis-backed token revocation via refresh logic.

### Styling & Design System
- UnoCSS resets provide consistent base styling.
- Utility classes (Tailwind-like) enabled through Uno presets (`presetUno`, `presetAttributify`, `presetIcons`).
- Custom tokens, breakpoints, and shortcuts extendable in `uno.config.ts`.

### Testing & Developer Commands
- Tests located under `tests/unit/` (Vitest) and `tests/e2e/` (Playwright scaffolding).
- Common commands:
  - `pnpm install` – install dependencies.
  - `pnpm dev` – start Vite dev server.
  - `pnpm build` – run `vue-tsc` type check then build production bundle.
  - `pnpm lint` – execute ESLint over `.ts` and `.vue` files.
  - `pnpm test:unit` / `pnpm test:e2e` – run Vitest or Playwright suites.

---

This document should be updated whenever new modules, tools, or architectural decisions are introduced. Pair it with ADRs in `docs/architecture-decision-records/` for contextual history.


