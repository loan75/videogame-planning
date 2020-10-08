"""Remove firm field

Revision ID: 1ea7af088aea
Revises: 838f3e5b01b4
Create Date: 2020-10-08 17:37:48.760549

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1ea7af088aea'
down_revision = '838f3e5b01b4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('platforms', 'firm')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('platforms', sa.Column('firm', sa.VARCHAR(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###