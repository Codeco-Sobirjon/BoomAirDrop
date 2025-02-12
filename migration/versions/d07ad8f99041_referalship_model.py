"""Referalship model

Revision ID: d07ad8f99041
Revises: ef2feff17434
Create Date: 2024-07-11 19:33:22.066858

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd07ad8f99041'
down_revision: Union[str, None] = 'ef2feff17434'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('referal',
    sa.Column('invitor_id', sa.BigInteger(), nullable=False),
    sa.Column('referal_id', sa.BigInteger(), nullable=False),
    sa.Column('interest_earned', sa.BigInteger(), nullable=False),
    sa.Column('invitation_reward', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['invitor_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['referal_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('invitor_id', 'referal_id')
    )
    op.create_index(op.f('ix_referal_invitor_id'), 'referal', ['invitor_id'], unique=False)
    op.create_index(op.f('ix_referal_referal_id'), 'referal', ['referal_id'], unique=False)
    op.drop_table('game_status')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('game_status',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('total_users', sa.BIGINT(), autoincrement=False, nullable=False),
    sa.Column('total_balance', sa.BIGINT(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='game_status_pkey')
    )
    op.drop_index(op.f('ix_referal_referal_id'), table_name='referal')
    op.drop_index(op.f('ix_referal_invitor_id'), table_name='referal')
    op.drop_table('referal')
    # ### end Alembic commands ###
