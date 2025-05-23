"""add: department model

Revision ID: c0b5b72ca182
Revises: 0e6455af1bf1
Create Date: 2025-04-13 22:44:04.368790

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c0b5b72ca182'
down_revision: Union[str, None] = '0e6455af1bf1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('departments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.Column('team_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['team_id'], ['teams.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('memberships', sa.Column('department_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'memberships', 'departments', ['department_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'memberships', type_='foreignkey')
    op.drop_column('memberships', 'department_id')
    op.drop_table('departments')
    # ### end Alembic commands ###
