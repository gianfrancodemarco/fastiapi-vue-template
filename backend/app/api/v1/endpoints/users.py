from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_session
from app.infrastructure.db.repositories.users import UserRepository
from app.schemas.user import UserRead


router = APIRouter()


@router.get("/me", response_model=UserRead)
async def read_current_user(current_user: UserRead = Depends(get_current_user)) -> UserRead:
    return current_user


@router.get("", response_model=list[UserRead])
async def list_users(
    current_user: UserRead = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> list[UserRead]:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough privileges")
    repo = UserRepository(session)
    users = await repo.list()
    return [UserRead.model_validate(user) for user in users]
