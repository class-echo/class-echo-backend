"""set default for created_at for students model

Revision ID: 903e41fdc11a
Revises: 241f1528fb85
Create Date: 2025-08-09 23:59:22.402994

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '903e41fdc11a'
down_revision: Union[str, Sequence[str], None] = '241f1528fb85'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        'students', 
        'created_at',
        server_default=sa.text('now()')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        'students', 
        'created_at',
        server_default=None
    )
