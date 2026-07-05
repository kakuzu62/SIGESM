from __future__ import annotations

from sqlalchemy.orm import configure_mappers


class MapperRegistry:
    """Coordinates SQLAlchemy mapper configuration."""

    @staticmethod
    def configure() -> None:
        """Configure all known ORM mappers."""
        configure_mappers()
