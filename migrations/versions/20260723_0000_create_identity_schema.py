"""Create identity schema baseline.

Revision ID: 20260723_0000
Revises:
Create Date: 2026-07-23
"""

from __future__ import annotations

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa

revision: str = "20260723_0000"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Create the initial Identity tables used by the first Identity releases."""
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
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_identity_users_username", "identity_users", ["username"], unique=True)
    op.create_index("ix_identity_users_email", "identity_users", ["email"], unique=True)

    op.create_table(
        "identity_roles",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("description", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_identity_roles_name", "identity_roles", ["name"], unique=True)

    op.create_table(
        "identity_permissions",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("code", sa.String(length=100), nullable=False),
        sa.Column("description", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_identity_permissions_code",
        "identity_permissions",
        ["code"],
        unique=True,
    )

    op.create_table(
        "identity_user_roles",
        sa.Column("user_id", sa.String(length=36), nullable=False),
        sa.Column("role_id", sa.String(length=36), nullable=False),
        sa.ForeignKeyConstraint(["role_id"], ["identity_roles.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["identity_users.id"]),
        sa.PrimaryKeyConstraint("user_id", "role_id"),
    )

    op.create_table(
        "identity_role_permissions",
        sa.Column("role_id", sa.String(length=36), nullable=False),
        sa.Column("permission_id", sa.String(length=36), nullable=False),
        sa.ForeignKeyConstraint(["permission_id"], ["identity_permissions.id"]),
        sa.ForeignKeyConstraint(["role_id"], ["identity_roles.id"]),
        sa.PrimaryKeyConstraint("role_id", "permission_id"),
    )

    op.create_table(
        "identity_user_sessions",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("user_id", sa.String(length=36), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("ended_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["identity_users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_identity_user_sessions_user_id",
        "identity_user_sessions",
        ["user_id"],
        unique=False,
    )

    op.create_table(
        "identity_authentication_sessions",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("user_id", sa.String(length=36), nullable=False),
        sa.Column("token_hash", sa.String(length=64), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_identity_authentication_sessions_user_id",
        "identity_authentication_sessions",
        ["user_id"],
        unique=False,
    )
    op.create_index(
        "ix_identity_authentication_sessions_token_hash",
        "identity_authentication_sessions",
        ["token_hash"],
        unique=True,
    )
    op.create_index(
        "ix_identity_authentication_sessions_expires_at",
        "identity_authentication_sessions",
        ["expires_at"],
        unique=False,
    )

    op.create_table(
        "identity_refresh_sessions",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("user_id", sa.String(length=36), nullable=False),
        sa.Column("session_id", sa.String(length=36), nullable=False),
        sa.Column("token_hash", sa.String(length=64), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_identity_refresh_sessions_user_id",
        "identity_refresh_sessions",
        ["user_id"],
        unique=False,
    )
    op.create_index(
        "ix_identity_refresh_sessions_session_id",
        "identity_refresh_sessions",
        ["session_id"],
        unique=False,
    )
    op.create_index(
        "ix_identity_refresh_sessions_token_hash",
        "identity_refresh_sessions",
        ["token_hash"],
        unique=True,
    )
    op.create_index(
        "ix_identity_refresh_sessions_expires_at",
        "identity_refresh_sessions",
        ["expires_at"],
        unique=False,
    )

    op.create_table(
        "identity_password_reset_requests",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("user_id", sa.String(length=36), nullable=False),
        sa.Column("token_hash", sa.String(length=64), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("used_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_identity_password_reset_requests_user_id",
        "identity_password_reset_requests",
        ["user_id"],
        unique=False,
    )
    op.create_index(
        "ix_identity_password_reset_requests_token_hash",
        "identity_password_reset_requests",
        ["token_hash"],
        unique=True,
    )
    op.create_index(
        "ix_identity_password_reset_requests_expires_at",
        "identity_password_reset_requests",
        ["expires_at"],
        unique=False,
    )

    op.create_table(
        "identity_authentication_attempts",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("username", sa.String(length=64), nullable=False),
        sa.Column("successful", sa.Boolean(), nullable=False),
        sa.Column("reason", sa.String(length=100), nullable=False),
        sa.Column("occurred_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_identity_authentication_attempts_username",
        "identity_authentication_attempts",
        ["username"],
        unique=False,
    )
    op.create_index(
        "ix_identity_authentication_attempts_occurred_at",
        "identity_authentication_attempts",
        ["occurred_at"],
        unique=False,
    )


def downgrade() -> None:
    """Drop the initial Identity tables."""
    op.drop_index(
        "ix_identity_authentication_attempts_occurred_at", "identity_authentication_attempts"
    )
    op.drop_index(
        "ix_identity_authentication_attempts_username", "identity_authentication_attempts"
    )
    op.drop_table("identity_authentication_attempts")

    op.drop_index(
        "ix_identity_password_reset_requests_expires_at", "identity_password_reset_requests"
    )
    op.drop_index(
        "ix_identity_password_reset_requests_token_hash", "identity_password_reset_requests"
    )
    op.drop_index("ix_identity_password_reset_requests_user_id", "identity_password_reset_requests")
    op.drop_table("identity_password_reset_requests")

    op.drop_index("ix_identity_refresh_sessions_expires_at", "identity_refresh_sessions")
    op.drop_index("ix_identity_refresh_sessions_token_hash", "identity_refresh_sessions")
    op.drop_index("ix_identity_refresh_sessions_session_id", "identity_refresh_sessions")
    op.drop_index("ix_identity_refresh_sessions_user_id", "identity_refresh_sessions")
    op.drop_table("identity_refresh_sessions")

    op.drop_index(
        "ix_identity_authentication_sessions_expires_at", "identity_authentication_sessions"
    )
    op.drop_index(
        "ix_identity_authentication_sessions_token_hash", "identity_authentication_sessions"
    )
    op.drop_index("ix_identity_authentication_sessions_user_id", "identity_authentication_sessions")
    op.drop_table("identity_authentication_sessions")

    op.drop_index("ix_identity_user_sessions_user_id", "identity_user_sessions")
    op.drop_table("identity_user_sessions")
    op.drop_table("identity_role_permissions")
    op.drop_table("identity_user_roles")

    op.drop_index("ix_identity_permissions_code", "identity_permissions")
    op.drop_table("identity_permissions")

    op.drop_index("ix_identity_roles_name", "identity_roles")
    op.drop_table("identity_roles")

    op.drop_index("ix_identity_users_email", "identity_users")
    op.drop_index("ix_identity_users_username", "identity_users")
    op.drop_table("identity_users")
