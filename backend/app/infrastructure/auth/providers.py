from __future__ import annotations

from dataclasses import dataclass


@dataclass
class EmailProvider:
    host: str
    port: int
    username: str | None = None
    password: str | None = None

    async def send_welcome_email(self, *, to_email: str) -> None:
        # Placeholder implementation for template consumers to extend.
        return None
