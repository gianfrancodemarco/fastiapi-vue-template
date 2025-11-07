from __future__ import annotations

from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logging import get_logger
from app.core.security import get_password_hash, verify_password
from app.domain.models.user import User
from app.infrastructure.db.repositories.users import UserRepository
from app.schemas.user import UserCreate

logger = get_logger(__name__)


class UserService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.users = UserRepository(session)

    async def register_user(self, payload: UserCreate) -> User:
        existing = await self.users.get_by_email(payload.email)
        if existing:
            msg = "User with this email already exists"
            raise ValueError(msg)

        hashed_password = get_password_hash(payload.password)
        user = await self.users.create(
            email=payload.email,
            hashed_password=hashed_password,
            full_name=payload.full_name,
        )
        await self.session.commit()
        await self.session.refresh(user)
        logger.info("user.created", user_id=user.id, email=user.email)
        return user

    async def authenticate(self, email: str, password: str) -> User | None:
        user = await self.users.get_by_email(email)
        if user is None:
            return None
        if not user.is_active:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        user.last_login_at = datetime.now(UTC)
        await self.session.flush()
        await self.session.commit()
        return user

    async def get_user(self, user_id: UUID) -> User | None:
        return await self.users.get(user_id)

    async def list_users(self) -> list[User]:
        return list(await self.users.list())
