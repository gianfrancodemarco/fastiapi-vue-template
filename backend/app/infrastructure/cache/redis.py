from __future__ import annotations

from functools import lru_cache

from redis.asyncio import Redis

from app.core.config import settings


@lru_cache(1)
def _client() -> Redis:
    return Redis.from_url(settings.redis_url, decode_responses=True)


async def get_redis_client() -> Redis:
    return _client()


async def close_redis_client() -> None:
    if _client.cache_info().currsize:
        client = _client()
        await client.aclose()
        _client.cache_clear()
