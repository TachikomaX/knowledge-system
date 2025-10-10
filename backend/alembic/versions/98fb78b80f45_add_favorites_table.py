"""add favorites table

Revision ID: 98fb78b80f45
Revises: b267a5c15845
Create Date: 2025-10-10 10:47:00.196043

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '98fb78b80f45'
down_revision: Union[str, Sequence[str], None] = 'b267a5c15845'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "favorites", sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("user_id",
                  sa.Integer,
                  sa.ForeignKey("users.id", ondelete="CASCADE"),
                  nullable=False),
        sa.Column("note_id",
                  sa.Integer,
                  sa.ForeignKey("notes.id", ondelete="CASCADE"),
                  nullable=False),
        sa.Column("created_at",
                  sa.DateTime(timezone=True),
                  server_default=sa.func.now()),
        sa.UniqueConstraint("user_id", "note_id",
                            name="uq_user_note_favorite"))


def downgrade() -> None:
    op.drop_table("favorites")
