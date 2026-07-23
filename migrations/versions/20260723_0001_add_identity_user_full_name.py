"""Add full name to identity users.

Revision ID: 20260723_0001
Revises:
Create Date: 2026-07-23
"""

from __future__ import annotations

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa

revision: str = "20260723_0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Add the full_name column preserving existing users."""
    op.add_column(
        "identity_users",
        sa.Column("full_name", sa.String(length=120), nullable=True),
    )
    op.execute("UPDATE identity_users SET full_name = username WHERE full_name IS NULL")
    with op.batch_alter_table("identity_users") as batch_op:
        batch_op.alter_column("full_name", existing_type=sa.String(length=120), nullable=False)


def downgrade() -> None:
    """Remove the full_name column."""
    with op.batch_alter_table("identity_users") as batch_op:
        batch_op.drop_column("full_name")
