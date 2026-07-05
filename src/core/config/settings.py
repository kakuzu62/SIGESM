from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True, frozen=True)
class DatabaseSettings:
    provider: str = "sqlite"
    database: str = "database/sigesm.db"
    echo: bool = False


@dataclass(slots=True, frozen=True)
class ApplicationSettings:
    name: str = "SIGESM Enterprise"
    version: str = "1.0.0"
    organization: str = "SIGESM"
    environment: str = "Development"
    debug: bool = True
    database: DatabaseSettings = field(default_factory=DatabaseSettings)


settings = ApplicationSettings()
