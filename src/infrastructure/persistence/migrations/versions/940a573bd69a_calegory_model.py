"""calegory_model

Revision ID: 940a573bd69a
Revises: 60c0e9d8c7bd
Create Date: 2025-09-25 22:42:54.172057

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '940a573bd69a'
down_revision: Union[str, Sequence[str], None] = '60c0e9d8c7bd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
