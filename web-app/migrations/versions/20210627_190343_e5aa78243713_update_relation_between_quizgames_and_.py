"""Update Relation between quizgames and quizgamequestions table

Revision ID: e5aa78243713
Revises: ce725aa41326
Create Date: 2021-06-27 19:03:43.113820

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e5aa78243713'
down_revision = 'ce725aa41326'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('quiz_game_quiz_game_questions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('quizgame_id', sa.Integer(), nullable=True),
    sa.Column('quizgamequestion_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['quizgame_id'], ['quiz_games.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['quizgamequestion_id'], ['quiz_game_questions.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_constraint('quiz_games_quizgame_question_id_fkey', 'quiz_games', type_='foreignkey')
    op.drop_column('quiz_games', 'quizgame_question_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('quiz_games', sa.Column('quizgame_question_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.create_foreign_key('quiz_games_quizgame_question_id_fkey', 'quiz_games', 'quiz_game_questions', ['quizgame_question_id'], ['id'])
    op.drop_table('quiz_game_quiz_game_questions')
    # ### end Alembic commands ###
