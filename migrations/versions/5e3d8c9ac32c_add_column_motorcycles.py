"""add_column_motorcycles

Revision ID: 5e3d8c9ac32c
Revises: 59a9b5a1b27e
Create Date: 2022-01-10 10:01:12.819232

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5e3d8c9ac32c'
down_revision = '59a9b5a1b27e'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('motorcycles', sa.Column('photo', sa.String))


def downgrade():
    op.remove_column('motorcycles','photo')
