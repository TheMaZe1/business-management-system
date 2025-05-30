"""fix length password

Revision ID: 5501def9c200
Revises: e50c1ec633d2
Create Date: 2025-04-13 14:52:26.730284

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5501def9c200'
down_revision: Union[str, None] = 'e50c1ec633d2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'password',
               existing_type=sa.VARCHAR(length=30),
               type_=sa.String(length=128),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'password',
               existing_type=sa.String(length=128),
               type_=sa.VARCHAR(length=30),
               existing_nullable=False)
    # ### end Alembic commands ###
