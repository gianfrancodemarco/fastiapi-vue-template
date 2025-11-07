# syntax=docker/dockerfile:1.7-labs

FROM python:3.13-slim AS base

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    UV_LINK_MODE=copy

RUN apt-get update && apt-get install -y --no-install-recommends build-essential curl && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip && pip install uv

WORKDIR /app

COPY pyproject.toml ./
COPY app ./app

RUN uv pip install --system --no-cache .

COPY alembic ./alembic
COPY alembic.ini ./alembic.ini
COPY app ./app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]


