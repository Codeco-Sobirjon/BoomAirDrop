"""Add geme status

Revision ID: 3f3ce979488a
Revises: c59cfc849958
Create Date: 2024-07-10 17:10:46.227984

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3f3ce979488a'
down_revision: Union[str, None] = 'c59cfc849958'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('game_status',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('total_users', sa.BigInteger(), nullable=False),
    sa.Column('total_balance', sa.BigInteger(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('game_status')
    # ### end Alembic commands ###
