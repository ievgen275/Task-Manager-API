"""added new collum in task

Revision ID: 75a75047909c
Revises: a27123752e98
Create Date: 2025-03-19 19:02:03.854833

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '75a75047909c'
down_revision: Union[str, None] = 'a27123752e98'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tasks', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'tasks', 'users', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'tasks', type_='foreignkey')
    op.drop_column('tasks', 'user_id')
    # ### end Alembic commands ###
