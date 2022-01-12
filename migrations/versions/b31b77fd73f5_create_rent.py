"""create-rent

Revision ID: b31b77fd73f5
Revises: 442340519f31
Create Date: 2022-01-09 16:21:47.563279

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b31b77fd73f5'
down_revision = '442340519f31'
branch_labels = None
depends_on = None



def upgrade():
    op.create_table(
        'rent',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, nullable=False),
        sa.Column('moto_id', sa.Integer, nullable=False),
        sa.Column('start_date', sa.String, nullable=False),
        sa.Column('end_date',sa.String, nullable=False),
        sa.Column('total_price',sa.Float, nullable=False),
        sa.Column('confirmed', sa.Boolean)
       
        
    )


def downgrade():
    op.drop_table('rent')
