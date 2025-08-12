"""Add auto increment to parent in created at field

Revision ID: 12f0ff2420ba
Revises: 0e46c1101fcc
Create Date: 2025-08-12 19:33:21.910645

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '12f0ff2420ba'
down_revision: Union[str, Sequence[str], None] = '0e46c1101fcc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        'parents', 
        'created_at',
        server_default=sa.text('now()')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        'parents', 
        'created_at',
        server_default=None
    )
