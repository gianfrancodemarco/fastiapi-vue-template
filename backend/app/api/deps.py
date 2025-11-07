from __future__ import annotations

from collections.abc import AsyncGenerator
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import decode_token, get_subject, get_token_identifier, is_token_type
from app.infrastructure.cache.redis import get_redis_client
from app.infrastructure.db.repositories.users import UserRepository
from app.infrastructure.db.session import SessionLocal
from app.schemas.user import UserRead
from app.services.auth import AuthService


bearer_scheme = HTTPBearer(auto_error=False)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session


async def get_redis() -> Redis:
    return await get_redis_client()


async def get_auth_service(
    session: AsyncSession = Depends(get_session),
    redis: Redis = Depends(get_redis),
) -> AuthService:
    return AuthService(session, redis)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    session: AsyncSession = Depends(get_session),
    redis: Redis = Depends(get_redis),
) -> UserRead:
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing credentials")

    token = credentials.credentials
    try:
        payload = decode_token(token)
    except Exception as exc:  # noqa: BLE001 - propagate as 401
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token") from exc

    if not is_token_type(payload, "access"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong token type")

    token_id = get_token_identifier(payload)
    cache_key = f"access:{token_id}"
    cached_user_id = await redis.get(cache_key)
    if cached_user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")

    subject = UUID(get_subject(payload))
    user_repo = UserRepository(session)
    user = await user_repo.get(subject)
    if user is None or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Inactive user")

    return UserRead.model_validate(user)
