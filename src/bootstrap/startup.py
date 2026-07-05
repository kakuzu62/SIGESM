from __future__ import annotations

from core.config.loader import Loader
from core.config.settings import settings
from core.logging.logger import configure_logging


class Startup:
    def initialize(self) -> None:
        Loader.initialize()

        configure_logging()

        print(
            f"""
========================================

SIGESM Enterprise

Environment : {settings.environment}
Database    : {settings.database.provider}

========================================
"""
        )
