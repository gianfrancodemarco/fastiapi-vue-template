from __future__ import annotations

from datetime import datetime
from uuid import UUID

from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.logging import get_logger
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    get_subject,
    get_token_identifier,
    is_token_type,
)
from app.domain.models.user import User
from app.infrastructure.db.repositories.users import UserRepository
from app.schemas.token import TokenResponse
from app.schemas.user import UserCreate
from app.services.users import UserService

logger = get_logger(__name__)


class AuthService:
    def __init__(self, session: AsyncSession, redis: Redis) -> None:
        self.session = session
        self.redis = redis
        self.users = UserRepository(session)
        self.user_service = UserService(session)

    async def register(self, payload: UserCreate) -> User:
        user = await self.user_service.register_user(payload)
        return user

    async def login(self, email: str, password: str) -> TokenResponse:
        user = await self.user_service.authenticate(email, password)
        if user is None:
            msg = "Invalid credentials"
            raise ValueError(msg)
        token_response = await self._issue_tokens(user)
        logger.info("auth.login", user_id=user.id)
        return token_response

    async def refresh(self, refresh_token: str) -> TokenResponse:
        payload = decode_token(refresh_token)
        if not is_token_type(payload, "refresh"):
            msg = "Invalid token type"
            raise ValueError(msg)
        token_id = get_token_identifier(payload)
        subject = get_subject(payload)
        is_active = await self.users.is_refresh_token_active(token_id)
        if not is_active:
            msg = "Refresh token revoked"
            raise ValueError(msg)
        user = await self.users.get(UUID(subject))
        if user is None:
            msg = "User not found"
            raise ValueError(msg)
        await self.users.revoke_refresh_token(token_id)
        await self.session.commit()
        token_response = await self._issue_tokens(user)
        logger.info("auth.refresh", user_id=user.id,
                    old_token_id=str(token_id))
        return token_response

    async def logout(self, refresh_token: str) -> None:
        payload = decode_token(refresh_token)
        if not is_token_type(payload, "refresh"):
            return
        token_id = get_token_identifier(payload)
        await self.users.revoke_refresh_token(token_id)
        await self.session.commit()
        logger.info("auth.logout", token_id=str(token_id))

    async def _issue_tokens(self, user: User) -> TokenResponse:
        access = create_access_token(str(user.id))
        refresh = create_refresh_token(str(user.id))

        await self.users.save_refresh_token(
            user_id=user.id,
            token_id=UUID(refresh["jti"]),
            expires_at=refresh["expires"],
        )
        await self.session.commit()

        await self.redis.setex(
            f"access:{access['jti']}",
            settings.jwt_expires_in_seconds,
            str(user.id),
        )
        await self.redis.setex(
            f"refresh:{refresh['jti']}",
            settings.jwt_refresh_expires_in_seconds,
            str(user.id),
        )

        return TokenResponse(
            access_token=access["token"],
            refresh_token=refresh["token"],
            expires_at=access["expires"],
            refresh_expires_at=refresh["expires"],
        )
