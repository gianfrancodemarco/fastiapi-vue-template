.PHONY: dev backend frontend migrate lint test

PNPM := $(shell if command -v pnpm >/dev/null 2>&1; then printf 'pnpm'; else printf 'corepack pnpm'; fi)

backend:
	cd backend && uv run fastapi dev app/main.py

frontend:
	cd frontend && $(PNPM) dev

dev:
	DEBUGPY=1 docker compose up --build

migrate:
	cd backend && uv run alembic upgrade head

lint:
	cd backend && uv run --extra dev ruff check . && uv run --extra dev mypy app
	cd frontend && $(PNPM) lint

format:
	cd backend && uv run --extra dev ruff format .

test:
	cd backend && uv run --extra dev pytest
	cd frontend && $(PNPM) test:unit
