from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_at: datetime
    refresh_expires_at: datetime


class RefreshRequest(BaseModel):
    refresh_token: str


class TokenIntrospection(BaseModel):
    subject: UUID
    token_id: UUID
    token_type: str
    expires_at: datetime
