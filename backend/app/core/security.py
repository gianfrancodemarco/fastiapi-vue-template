from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any
from uuid import UUID, uuid4

import jwt
from passlib.context import CryptContext

from .config import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_token(*, subject: str, token_type: str, expires_delta: timedelta) -> dict[str, Any]:
    now = datetime.now(UTC)
    expire = now + expires_delta
    jti = str(uuid4())

    payload: dict[str, Any] = {
        "sub": subject,
        "iat": int(now.timestamp()),
        "exp": int(expire.timestamp()),
        "type": token_type,
        "jti": jti,
    }

    encoded = jwt.encode(payload, settings.jwt_secret,
                         algorithm=settings.jwt_algorithm)
    return {"token": encoded, "expires": expire, "jti": jti}


def create_access_token(subject: str) -> dict[str, Any]:
    expires = timedelta(seconds=settings.jwt_expires_in_seconds)
    return create_token(subject=subject, token_type="access", expires_delta=expires)


def create_refresh_token(subject: str) -> dict[str, Any]:
    expires = timedelta(seconds=settings.jwt_refresh_expires_in_seconds)
    return create_token(subject=subject, token_type="refresh", expires_delta=expires)


def decode_token(token: str) -> dict[str, Any]:
    return jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def is_token_type(token_payload: dict[str, Any], token_type: str) -> bool:
    return token_payload.get("type") == token_type


def get_subject(token_payload: dict[str, Any]) -> str:
    subject = token_payload.get("sub")
    if subject is None:
        msg = "Token payload missing subject"
        raise ValueError(msg)
    return subject


def get_token_identifier(token_payload: dict[str, Any]) -> UUID:
    token_id = token_payload.get("jti")
    if token_id is None:
        msg = "Token payload missing id"
        raise ValueError(msg)
    return UUID(token_id)
