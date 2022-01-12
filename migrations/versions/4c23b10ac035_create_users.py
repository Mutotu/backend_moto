"""create-users

Revision ID: 4c23b10ac035
Revises: 
Create Date: 2022-01-09 16:21:16.461072

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4c23b10ac035'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('first_name', sa.String(120), nullable=False),
        sa.Column('last_name', sa.String(120), nullable=False),
        sa.Column('age', sa.String, nullable=False),
        sa.Column('email', sa.String, nullable=False, unique=True),
        sa.Column('username',sa.String(120), nullable=False, unique=True),
        sa.Column('password', sa.String(120), nullable=False),
        sa.Column('role', sa.String, nullable=False)
    )


def downgrade():
    op.drop_table('users')
