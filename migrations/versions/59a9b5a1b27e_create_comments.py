"""create-comments

Revision ID: 59a9b5a1b27e
Revises: b31b77fd73f5
Create Date: 2022-01-09 16:21:55.605447

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '59a9b5a1b27e'
down_revision = 'b31b77fd73f5'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'comments',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id',sa.Integer, nullable=False),
        sa.Column('moto_id', sa.Integer, nullable=False),
        sa.Column('title', sa.String(20), nullable=False),
        sa.Column('comment', sa.String(120), nullable=False),
        sa.Column('date', sa.DateTime, nullable=False)
        )


def downgrade():
    op.drop_table('comments')
