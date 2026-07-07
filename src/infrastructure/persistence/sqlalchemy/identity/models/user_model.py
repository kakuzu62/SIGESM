from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database.base import Base

if TYPE_CHECKING:
    from infrastructure.persistence.sqlalchemy.identity.models.role_model import RoleModel
    from infrastructure.persistence.sqlalchemy.identity.models.user_session_model import (
        UserSessionModel,
    )

identity_user_roles = Table(
    "identity_user_roles",
    Base.metadata,
    Column("user_id", String(36), ForeignKey("identity_users.id"), primary_key=True),
    Column("role_id", String(36), ForeignKey("identity_roles.id"), primary_key=True),
)


class UserModel(Base):
    """SQLAlchemy model for users."""

    __tablename__ = "identity_users"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    username: Mapped[str] = mapped_column(String(64), nullable=False, unique=True, index=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(512), nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    failed_login_attempts: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    locked_until: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    roles: Mapped[list[RoleModel]] = relationship(
        secondary=identity_user_roles,
        back_populates="users",
    )
    sessions: Mapped[list[UserSessionModel]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )
