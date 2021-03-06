"""Add user_id Column to highscore_ranks Table

Revision ID: d0af6cad595b
Revises: 1a2932a77db7
Create Date: 2021-07-25 19:35:30.441972

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd0af6cad595b'
down_revision = '1a2932a77db7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('highscore_ranks', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_unique_constraint(None, 'highscore_ranks', ['user_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'highscore_ranks', type_='unique')
    op.drop_column('highscore_ranks', 'user_id')
    # ### end Alembic commands ###
