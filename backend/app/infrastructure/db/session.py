from __future__ import annotations

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings


def get_engine() -> AsyncEngine:
    return create_async_engine(settings.database_uri, echo=settings.debug, future=True)


engine: AsyncEngine = get_engine()
SessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session
