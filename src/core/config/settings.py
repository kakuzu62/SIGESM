from __future__ import annotations

from dataclasses import dataclass, field

from core.config.environment import Environment
from core.constants.application import APPLICATION_NAME, APPLICATION_VERSION, ORGANIZATION


@dataclass(slots=True, frozen=True)
class DatabaseSettings:
    """Database configuration loaded from environment variables."""

    provider: str = Environment.get("DATABASE_PROVIDER", "sqlite") or "sqlite"
    database: str = Environment.get("DATABASE_NAME", "database/sigesm.db") or "database/sigesm.db"
    host: str = Environment.get("DATABASE_HOST", "localhost") or "localhost"
    port: int = int(Environment.get("DATABASE_PORT", "5432") or "5432")
    username: str = Environment.get("DATABASE_USER", "") or ""
    password: str = Environment.get("DATABASE_PASSWORD", "") or ""
    echo: bool = Environment.get_bool("DATABASE_ECHO", False)
    pool_size: int = int(Environment.get("DATABASE_POOL_SIZE", "5") or "5")
    max_overflow: int = int(Environment.get("DATABASE_MAX_OVERFLOW", "10") or "10")
    pool_pre_ping: bool = Environment.get_bool("DATABASE_POOL_PRE_PING", True)

    @property
    def url(self) -> str:
        """Return the SQLAlchemy database URL."""
        normalized_provider = self.provider.lower()

        if normalized_provider == "sqlite":
            return f"sqlite:///{self.database}"

        if normalized_provider in {"postgres", "postgresql"}:
            credentials = self.username
            if self.password:
                credentials = f"{credentials}:{self.password}"

            auth = f"{credentials}@" if credentials else ""
            return f"postgresql+psycopg://{auth}{self.host}:{self.port}/{self.database}"

        return self.database


@dataclass(slots=True, frozen=True)
class ApplicationSettings:
    """Application settings used during startup and dependency wiring."""

    name: str = Environment.get("APP_NAME", APPLICATION_NAME) or APPLICATION_NAME
    version: str = APPLICATION_VERSION
    organization: str = ORGANIZATION
    environment: str = Environment.get("APP_ENV", "Development") or "Development"
    debug: bool = Environment.get_bool("APP_DEBUG", True)
    database: DatabaseSettings = field(default_factory=DatabaseSettings)


settings = ApplicationSettings()
