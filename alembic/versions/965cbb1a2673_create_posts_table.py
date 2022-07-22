"""create posts table

Revision ID: 965cbb1a2673
Revises: 
Create Date: 2022-07-22 17:59:23.340081

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '965cbb1a2673'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False,
                    primary_key=True), sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_table('posts')
    pass