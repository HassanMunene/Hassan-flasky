"""added the email field in the user model

Revision ID: 9b11666e3bad
Revises: 5d2ed0b36471
Create Date: 2023-09-07 11:05:48.797336

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9b11666e3bad'
down_revision = '5d2ed0b36471'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('email', sa.String(length=64), nullable=True))
        batch_op.add_column(sa.Column('password_hash', sa.String(length=128), nullable=True))
        batch_op.create_index(batch_op.f('ix_users_email'), ['email'], unique=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_users_email'))
        batch_op.drop_column('password_hash')
        batch_op.drop_column('email')

    # ### end Alembic commands ###
