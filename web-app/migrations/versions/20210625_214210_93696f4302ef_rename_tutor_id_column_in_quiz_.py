"""Rename tutor_id column in quiz_questions table

Revision ID: 93696f4302ef
Revises: 74ab77a114f0
Create Date: 2021-06-25 21:42:10.615958

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '93696f4302ef'
down_revision = '74ab77a114f0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('quiz_questions', sa.Column('tutor_id', sa.Integer(), nullable=False))
    op.drop_constraint('quiz_questions_user_id_fkey', 'quiz_questions', type_='foreignkey')
    op.create_foreign_key(None, 'quiz_questions', 'users', ['tutor_id'], ['id'])
    op.drop_column('quiz_questions', 'user_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('quiz_questions', sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'quiz_questions', type_='foreignkey')
    op.create_foreign_key('quiz_questions_user_id_fkey', 'quiz_questions', 'users', ['user_id'], ['id'])
    op.drop_column('quiz_questions', 'tutor_id')
    # ### end Alembic commands ###
