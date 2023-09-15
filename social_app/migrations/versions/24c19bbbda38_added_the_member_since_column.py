"""added the member since column

Revision ID: 24c19bbbda38
Revises: cb0c2271348c
Create Date: 2023-09-14 12:10:52.319680

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '24c19bbbda38'
down_revision = 'cb0c2271348c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('member_since', sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('member_since')

    # ### end Alembic commands ###