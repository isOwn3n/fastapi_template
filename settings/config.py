from typing import Any
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "sqlite+aiosqlite:///database.sqlite3"
    database_connection_args: dict[str, Any] = {"check_same_thread": False}
    debug: bool = True
    secret: str = "secret"
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        extra="ignore",
    )


config = Settings()
