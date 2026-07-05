from __future__ import annotations

from pathlib import Path

from core.config.paths import RESOURCES


class ResourceManager:
    @staticmethod
    def resource(name: str) -> Path:
        return RESOURCES / name
