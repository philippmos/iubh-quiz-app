"""Add QuizSuggestions and QuizSuggestionAnswers Table

Revision ID: 74f2412ed0bc
Revises: 179266ed1559
Create Date: 2021-06-05 11:29:12.787564

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '74f2412ed0bc'
down_revision = '179266ed1559'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('quiz_suggestions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('question', sa.String(), nullable=False),
    sa.Column('creation_date', sa.DateTime(), nullable=True),
    sa.Column('is_approved', sa.Boolean(), nullable=True),
    sa.Column('is_declined', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('question')
    )
    op.create_table('quiz_suggestion_answers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('text', sa.String(), nullable=False),
    sa.Column('is_correct', sa.Boolean(), nullable=True),
    sa.Column('quiz_suggestion_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['quiz_suggestion_id'], ['quiz_suggestions.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('quiz_suggestion_answers')
    op.drop_table('quiz_suggestions')
    # ### end Alembic commands ###