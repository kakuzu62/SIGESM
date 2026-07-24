"""Add role assignment metadata.

Revision ID: 20260723_0002
Revises: 20260723_0001
Create Date: 2026-07-23
"""

from __future__ import annotations

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa

revision: str = "20260723_0002"
down_revision: str | None = "20260723_0001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Add normalized role name and active flag."""
    op.add_column(
        "identity_roles",
        sa.Column("normalized_name", sa.String(length=100), nullable=True),
    )
    op.add_column(
        "identity_roles",
        sa.Column("active", sa.Boolean(), nullable=False, server_default=sa.true()),
    )
    op.execute(
        "UPDATE identity_roles SET normalized_name = UPPER(TRIM(name)) "
        "WHERE normalized_name IS NULL"
    )
    with op.batch_alter_table("identity_roles") as batch_op:
        batch_op.alter_column(
            "normalized_name",
            existing_type=sa.String(length=100),
            nullable=False,
        )
        batch_op.create_index(
            "ix_identity_roles_normalized_name",
            ["normalized_name"],
            unique=True,
        )


def downgrade() -> None:
    """Remove role assignment metadata."""
    with op.batch_alter_table("identity_roles") as batch_op:
        batch_op.drop_index("ix_identity_roles_normalized_name")
        batch_op.drop_column("active")
        batch_op.drop_column("normalized_name")
