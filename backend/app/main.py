from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.api.router import api_router
from app.core.config import settings
from app.core.logging import configure_logging, get_logger
from app.infrastructure.cache.redis import close_redis_client
from app.infrastructure.db.session import engine

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI):
    configure_logging()
    logger.info("app.startup")
    async with engine.begin() as conn:
        await conn.execute(text("SELECT 1"))
    try:
        yield
    finally:
        await engine.dispose()
        await close_redis_client()
        logger.info("app.shutdown")


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    debug=settings.debug,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors.allow_origins,
    allow_credentials=settings.cors.allow_credentials,
    allow_methods=settings.cors.allow_methods,
    allow_headers=settings.cors.allow_headers,
)

app.include_router(api_router, prefix="/api")


@app.get("/", tags=["health"])
async def root() -> dict[str, str]:
    return {"message": "FastAPI Vue Template backend"}
