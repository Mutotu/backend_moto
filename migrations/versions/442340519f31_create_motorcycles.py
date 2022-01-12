"""create-motorcycles

Revision ID: 442340519f31
Revises: 4c23b10ac035
Create Date: 2022-01-09 16:21:41.749476

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '442340519f31'
down_revision = '4c23b10ac035'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('motorcycles',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, nullable=False),
        sa.Column('make', sa.String, nullable=False),
        sa.Column('model', sa.String, nullable=False),
        sa.Column('year',sa.String, nullable=False),
        sa.Column('price',sa.Float, nullable=False),
        sa.Column('description',sa.String, nullable=False),
                    )


def downgrade():
    op.drop_table('motorcycles')
