from __future__ import annotations

import logging
from collections.abc import Callable


class ApplicationLifecycle:
    """Coordinates desktop startup, shutdown and exception logging."""

    def __init__(self) -> None:
        self._logger = logging.getLogger(__name__)

    def startup(self) -> None:
        """Log desktop startup."""
        self._logger.info("SIGESM desktop startup started.")

    def shutdown(self) -> None:
        """Log desktop shutdown."""
        self._logger.info("SIGESM desktop shutdown completed.")

    def run_guarded(self, action: Callable[[], int]) -> int:
        """Run an application action with global exception handling."""
        try:
            self.startup()
            return action()
        except Exception:
            self._logger.exception("Unhandled desktop application error.")
            raise
        finally:
            self.shutdown()
