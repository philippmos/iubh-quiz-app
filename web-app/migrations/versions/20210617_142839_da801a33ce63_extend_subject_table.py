"""extend subject table

Revision ID: da801a33ce63
Revises: 6b675f132a29
Create Date: 2021-06-17 14:28:39.401864

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'da801a33ce63'
down_revision = '6b675f132a29'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('subjects', sa.Column('short', sa.String(length=20), nullable=False))
    op.add_column('subjects', sa.Column('image_path', sa.String(length=255), nullable=False))
    op.add_column('subjects', sa.Column('tutor_id', sa.Integer(), nullable=False))
    op.create_unique_constraint(None, 'subjects', ['short'])
    op.create_foreign_key(None, 'subjects', 'users', ['tutor_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'subjects', type_='foreignkey')
    op.drop_constraint(None, 'subjects', type_='unique')
    op.drop_column('subjects', 'tutor_id')
    op.drop_column('subjects', 'image_path')
    op.drop_column('subjects', 'short')
    # ### end Alembic commands ###