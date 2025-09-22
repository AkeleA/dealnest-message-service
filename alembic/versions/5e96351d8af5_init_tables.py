"""init tables

Revision ID: 5e96351d8af5
Revises: 60c38927fbe6
Create Date: 2025-09-22 08:46:43.588720

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5e96351d8af5'
down_revision: Union[str, Sequence[str], None] = '60c38927fbe6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
