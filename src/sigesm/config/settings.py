from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    url: str = Field(default="sqlite:///database/sigesm.db", alias="SIGESM_DATABASE_URL")
    echo: bool = Field(default=False, alias="SIGESM_DATABASE_ECHO")
    pool_pre_ping: bool = Field(default=True, alias="SIGESM_DATABASE_POOL_PRE_PING")

    model_config = SettingsConfigDict(extra="ignore", populate_by_name=True)

    @property
    def is_sqlite(self) -> bool:
        return self.url.startswith("sqlite")


class Settings(BaseSettings):
    app_name: str = Field(default="SIGESM Enterprise", alias="SIGESM_APP_NAME")
    environment: str = Field(default="development", alias="SIGESM_ENVIRONMENT")
    project_root: Path = Field(default_factory=lambda: Path.cwd())
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        populate_by_name=True,
    )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
