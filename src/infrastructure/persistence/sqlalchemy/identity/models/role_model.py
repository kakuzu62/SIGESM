from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Column, DateTime, ForeignKey, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database.base import Base

if TYPE_CHECKING:
    from infrastructure.persistence.sqlalchemy.identity.models.permission_model import (
        PermissionModel,
    )
    from infrastructure.persistence.sqlalchemy.identity.models.user_model import UserModel

identity_role_permissions = Table(
    "identity_role_permissions",
    Base.metadata,
    Column("role_id", String(36), ForeignKey("identity_roles.id"), primary_key=True),
    Column(
        "permission_id",
        String(36),
        ForeignKey("identity_permissions.id"),
        primary_key=True,
    ),
)


class RoleModel(Base):
    """SQLAlchemy model for roles."""

    __tablename__ = "identity_roles"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, index=True)
    description: Mapped[str] = mapped_column(String(255), nullable=False, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    permissions: Mapped[list[PermissionModel]] = relationship(
        secondary=identity_role_permissions,
        back_populates="roles",
    )
    users: Mapped[list[UserModel]] = relationship(
        secondary="identity_user_roles",
        back_populates="roles",
    )
