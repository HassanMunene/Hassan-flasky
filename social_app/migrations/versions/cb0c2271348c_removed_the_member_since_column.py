"""removed the member since column

Revision ID: cb0c2271348c
Revises: 19264cb5b0d2
Create Date: 2023-09-14 12:09:23.484799

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'cb0c2271348c'
down_revision = '19264cb5b0d2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('Member_since')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('Member_since', mysql.DATETIME(), nullable=True))

    # ### end Alembic commands ###