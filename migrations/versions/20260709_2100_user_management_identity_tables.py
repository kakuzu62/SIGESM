"""Create identity tables for user management.

Revision ID: 20260709_2100
Revises:
Create Date: 2026-07-09 21:00:00.000000
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260709_2100"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Create identity tables."""
    op.create_table(
        "identity_roles",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("description", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_identity_roles")),
        sa.UniqueConstraint("name", name=op.f("uq_identity_roles_name")),
    )
    op.create_index(op.f("ix_identity_roles_name"), "identity_roles", ["name"], unique=False)
    op.create_table(
        "identity_permissions",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("code", sa.String(length=120), nullable=False),
        sa.Column("description", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_identity_permissions")),
        sa.UniqueConstraint("code", name=op.f("uq_identity_permissions_code")),
    )
    op.create_index(
        op.f("ix_identity_permissions_code"), "identity_permissions", ["code"], unique=False
    )
    op.create_table(
        "identity_users",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("username", sa.String(length=64), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("password_hash", sa.String(length=512), nullable=False),
        sa.Column("active", sa.Boolean(), nullable=False),
        sa.Column("failed_login_attempts", sa.Integer(), nullable=False),
        sa.Column("locked_until", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_identity_users")),
        sa.UniqueConstraint("email", name=op.f("uq_identity_users_email")),
        sa.UniqueConstraint("username", name=op.f("uq_identity_users_username")),
    )
    op.create_index(op.f("ix_identity_users_email"), "identity_users", ["email"], unique=False)
    op.create_index(
        op.f("ix_identity_users_username"), "identity_users", ["username"], unique=False
    )
    op.create_table(
        "identity_user_roles",
        sa.Column("user_id", sa.String(length=36), nullable=False),
        sa.Column("role_id", sa.String(length=36), nullable=False),
        sa.ForeignKeyConstraint(
            ["role_id"],
            ["identity_roles.id"],
            name=op.f("fk_identity_user_roles_role_id_identity_roles"),
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["identity_users.id"],
            name=op.f("fk_identity_user_roles_user_id_identity_users"),
        ),
        sa.PrimaryKeyConstraint("user_id", "role_id", name=op.f("pk_identity_user_roles")),
    )
    op.create_table(
        "identity_role_permissions",
        sa.Column("role_id", sa.String(length=36), nullable=False),
        sa.Column("permission_id", sa.String(length=36), nullable=False),
        sa.ForeignKeyConstraint(
            ["permission_id"],
            ["identity_permissions.id"],
            name=op.f("fk_identity_role_permissions_permission_id_identity_permissions"),
        ),
        sa.ForeignKeyConstraint(
            ["role_id"],
            ["identity_roles.id"],
            name=op.f("fk_identity_role_permissions_role_id_identity_roles"),
        ),
        sa.PrimaryKeyConstraint(
            "role_id", "permission_id", name=op.f("pk_identity_role_permissions")
        ),
    )


def downgrade() -> None:
    """Drop identity tables."""
    op.drop_table("identity_role_permissions")
    op.drop_table("identity_user_roles")
    op.drop_index(op.f("ix_identity_users_username"), table_name="identity_users")
    op.drop_index(op.f("ix_identity_users_email"), table_name="identity_users")
    op.drop_table("identity_users")
    op.drop_index(op.f("ix_identity_permissions_code"), table_name="identity_permissions")
    op.drop_table("identity_permissions")
    op.drop_index(op.f("ix_identity_roles_name"), table_name="identity_roles")
    op.drop_table("identity_roles")
