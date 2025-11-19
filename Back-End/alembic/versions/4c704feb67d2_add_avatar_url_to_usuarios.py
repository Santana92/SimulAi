"""add_avatar_url_to_usuarios

Revision ID: 4c704feb67d2
Revises: 5a6544320289
Create Date: 2025-11-19 05:51:33.411339

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4c704feb67d2'
down_revision: Union[str, Sequence[str], None] = '5a6544320289'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('usuarios', sa.Column('avatar_url', sa.String(length=255), nullable=True))


def downgrade() -> None:
    op.drop_column('usuarios', 'avatar_url')