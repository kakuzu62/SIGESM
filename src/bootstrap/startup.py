from __future__ import annotations

import logging

from core.config.loader import Loader
from core.config.settings import settings
from core.logging.logger import configure_logging

logger = logging.getLogger(__name__)


class Startup:
    """Application startup coordinator."""

    def initialize(self) -> None:
        """Prepare filesystem, logging and startup diagnostics."""
        Loader.initialize()

        configure_logging()

        logger.info(
            "SIGESM Enterprise initialized. Environment=%s Database=%s",
            settings.environment,
            settings.database.provider,
        )
