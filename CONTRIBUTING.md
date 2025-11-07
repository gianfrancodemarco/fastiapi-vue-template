# Contributing

## Prerequisites

- Python 3.13+
- Node.js 22 with pnpm (`corepack enable`)
- Docker Engine 27+
- `uv` for Python dependency management

## Development Workflow

1. Fork and clone the repository.
2. Copy env templates: `cp backend/env.example backend/.env` and `cp frontend/.env.example frontend/.env`.
3. Start services with `docker compose up --build` or run backend/frontend locally.
4. Create a feature branch.
5. Run `make lint` and `make test` before submitting a PR.

## Commit Style

- Follow conventional commits when possible (`feat:`, `fix:`, `docs:`, etc.).
- Keep commits focused and include tests where applicable.

## Pull Requests

- Reference related issues.
- Describe the change and rationale clearly.
- Ensure CI passes (lint + tests).

## Code Style

- Python: enforced via `ruff`, `black`, `mypy`.
- TypeScript/Vue: enforced via ESLint + Prettier + UnoCSS conventions.

Thank you for helping improve the template!
