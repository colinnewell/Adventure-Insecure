"""empty message

Revision ID: 1e4c788b2c90
Revises: 3435de009558
Create Date: 2016-03-27 19:10:59.815913

"""

# revision identifiers, used by Alembic.
revision = '1e4c788b2c90'
down_revision = '3435de009558'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('signup_attempts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('date_modified', sa.DateTime(), nullable=True),
    sa.Column('email', sa.String(length=128), nullable=False),
    sa.Column('registration_code', sa.String(length=128), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('signup_attempts')
    ### end Alembic commands ###
