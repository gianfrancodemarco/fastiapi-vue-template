from __future__ import annotations

from functools import lru_cache
from typing import Any
from urllib.parse import quote_plus

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class CorsSettings(BaseModel):
    allow_origins: list[str] = Field(default_factory=lambda: [
                                     "http://localhost:5173"])
    allow_credentials: bool = True
    allow_methods: list[str] = Field(default_factory=lambda: ["*"])
    allow_headers: list[str] = Field(default_factory=lambda: ["*"])


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        env_nested_delimiter="__",
    )

    app_name: str = "FastAPI Vue Template"
    environment: str = "local"
    debug: bool = True

    database_host: str = "db"
    database_port: int = 5432
    database_user: str = "template"
    database_password: str = "template"
    database_name: str = "template"

    redis_url: str = "redis://redis:6379/0"

    jwt_secret: str = Field(default="change-me", alias="JWT_SECRET")
    jwt_algorithm: str = Field(default="HS256", alias="JWT_ALGORITHM")
    jwt_expires_in_seconds: int = Field(
        default=900, alias="JWT_EXPIRES_IN_SECONDS")
    jwt_refresh_expires_in_seconds: int = Field(
        default=604_800, alias="JWT_REFRESH_EXPIRES_IN_SECONDS")

    otlp_endpoint: str | None = Field(default=None, alias="OTLP_ENDPOINT")

    celery_broker_url: str = "redis://redis:6379/1"
    celery_result_backend: str = "redis://redis:6379/2"

    smtp_host: str | None = None
    smtp_port: int | None = None
    smtp_username: str | None = None
    smtp_password: str | None = None

    cors: CorsSettings = CorsSettings()

    def model_post_init(self, __context: Any) -> None:  # pragma: no cover - pydantic hook
        if isinstance(self.cors, dict):
            self.cors = CorsSettings(**self.cors)

    @property
    def database_uri(self) -> str:
        password = quote_plus(self.database_password)
        return (
            f"postgresql+psycopg_async://{self.database_user}:{password}"
            f"@{self.database_host}:{self.database_port}/{self.database_name}"
        )

    @property
    def sync_database_uri(self) -> str:
        password = quote_plus(self.database_password)
        return (
            f"postgresql+psycopg://{self.database_user}:{password}"
            f"@{self.database_host}:{self.database_port}/{self.database_name}"
        )


@lru_cache(1)
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
