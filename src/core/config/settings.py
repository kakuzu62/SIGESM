from __future__ import annotations

from dataclasses import dataclass, field

from core.config.environment import Environment
from core.constants.application import APPLICATION_NAME, APPLICATION_VERSION, ORGANIZATION


@dataclass(slots=True, frozen=True)
class DatabaseSettings:
    provider: str = Environment.get("DATABASE_PROVIDER", "sqlite") or "sqlite"
    database: str = Environment.get("DATABASE_NAME", "database/sigesm.db") or "database/sigesm.db"
    echo: bool = False


@dataclass(slots=True, frozen=True)
class ApplicationSettings:
    name: str = Environment.get("APP_NAME", APPLICATION_NAME) or APPLICATION_NAME
    version: str = APPLICATION_VERSION
    organization: str = ORGANIZATION
    environment: str = Environment.get("APP_ENV", "Development") or "Development"
    debug: bool = Environment.get_bool("APP_DEBUG", True)
    database: DatabaseSettings = field(default_factory=DatabaseSettings)


settings = ApplicationSettings()
