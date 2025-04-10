"""add audit fields to User

Revision ID: 37e111b196dd
Revises: 06b1b4ebf1d8
Create Date: 2025-04-07 10:19:05.019444

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '37e111b196dd'
down_revision: Union[str, None] = '06b1b4ebf1d8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False))
    op.add_column('users', sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('users', sa.Column('is_deleted', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'is_deleted')
    op.drop_column('users', 'deleted_at')
    op.drop_column('users', 'created_at')
    # ### end Alembic commands ###
