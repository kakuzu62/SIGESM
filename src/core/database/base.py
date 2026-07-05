from __future__ import annotations

from sqlalchemy.orm import DeclarativeBase

from core.database.metadata import metadata


class Base(DeclarativeBase):
    """Declarative base shared by every persistence model."""

    metadata = metadata
