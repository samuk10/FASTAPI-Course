"""add content column to posts table

Revision ID: cadc7093f3d7
Revises: 965cbb1a2673
Create Date: 2022-07-22 18:10:31.930989

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cadc7093f3d7'
down_revision = '965cbb1a2673'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass