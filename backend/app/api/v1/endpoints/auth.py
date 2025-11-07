from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_auth_service
from app.schemas.auth import LoginRequest
from app.schemas.token import RefreshRequest, TokenResponse
from app.schemas.user import UserCreate, UserRead
from app.services.auth import AuthService


router = APIRouter()


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register_user(
    payload: UserCreate,
    auth_service: AuthService = Depends(get_auth_service),
) -> UserRead:
    try:
        user = await auth_service.register(payload)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    return UserRead.model_validate(user)


@router.post("/login", response_model=TokenResponse)
async def login(
    payload: LoginRequest,
    auth_service: AuthService = Depends(get_auth_service),
) -> TokenResponse:
    try:
        return await auth_service.login(payload.email, payload.password)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    payload: RefreshRequest,
    auth_service: AuthService = Depends(get_auth_service),
) -> TokenResponse:
    try:
        return await auth_service.refresh(payload.refresh_token)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc


@router.post("/logout", status_code=status.HTTP_202_ACCEPTED)
async def logout(
    payload: RefreshRequest,
    auth_service: AuthService = Depends(get_auth_service),
) -> None:
    await auth_service.logout(payload.refresh_token)
