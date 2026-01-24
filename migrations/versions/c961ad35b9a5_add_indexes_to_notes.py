"""add indexes to notes

Revision ID: c961ad35b9a5
Revises: ce8a921a6aa8
Create Date: 2026-01-24 07:18:23.595536

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c961ad35b9a5'
down_revision: Union[str, Sequence[str], None] = 'ce8a921a6aa8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_index(
        "ix_notes_user_id",
        "notes",
        ["owner_id"]
    )
    op.create_index(
        "ix_notes_user_id_created_at",
        "notes",
        ["owner_id","created_at"]
    )


def downgrade() -> None:
    op.drop_index("ix_notes_user_id_created_at",table_name="notes")
    op.drop_index("ix_notes_user_id",table_name="notes")
