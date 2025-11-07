from __future__ import annotations

from datetime import UTC, datetime
from typing import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.models.refresh_token import RefreshToken
from app.domain.models.user import User


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get(self, user_id: UUID) -> User | None:
        result = await self.session.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> User | None:
        result = await self.session.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def list(self) -> Sequence[User]:
        result = await self.session.execute(select(User).order_by(User.created_at.desc()))
        return result.scalars().all()

    async def create(self, *, email: str, hashed_password: str, full_name: str | None = None) -> User:
        user = User(email=email, hashed_password=hashed_password,
                    full_name=full_name)
        self.session.add(user)
        await self.session.flush()
        return user

    async def save_refresh_token(
        self,
        *,
        user_id: UUID,
        token_id: UUID,
        expires_at: datetime,
    ) -> RefreshToken:
        refresh_token = RefreshToken(
            user_id=user_id,
            token_id=token_id,
            expires_at=expires_at,
        )
        self.session.add(refresh_token)
        await self.session.flush()
        return refresh_token

    async def revoke_refresh_token(self, token_id: UUID) -> None:
        result = await self.session.execute(
            select(RefreshToken).where(RefreshToken.token_id ==
                                       token_id, RefreshToken.revoked.is_(False))
        )
        refresh_token = result.scalar_one_or_none()
        if refresh_token is None:
            return
        refresh_token.revoked = True
        await self.session.flush()

    async def is_refresh_token_active(self, token_id: UUID) -> bool:
        result = await self.session.execute(
            select(RefreshToken)
            .where(
                RefreshToken.token_id == token_id,
                RefreshToken.revoked.is_(False),
                RefreshToken.expires_at > datetime.now(UTC),
            )
            .limit(1)
        )
        token = result.scalar_one_or_none()
        return token is not None
