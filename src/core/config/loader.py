from __future__ import annotations

from core.config.paths import CONFIG, DATABASE, LOGS


class Loader:
    @staticmethod
    def initialize() -> None:
        LOGS.mkdir(exist_ok=True)
        DATABASE.mkdir(exist_ok=True)
        CONFIG.mkdir(exist_ok=True)
