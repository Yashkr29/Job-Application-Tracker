"""Initial schema.

Revision ID: 0001_initial_schema
Revises:
Create Date: 2026-06-12
"""
from typing import Sequence, Union

from alembic import op

from app.core.database import Base
from app.models import *  # noqa: F403

revision: str = "0001_initial_schema"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create all tables."""
    Base.metadata.create_all(bind=op.get_bind())


def downgrade() -> None:
    """Drop all tables."""
    Base.metadata.drop_all(bind=op.get_bind())

