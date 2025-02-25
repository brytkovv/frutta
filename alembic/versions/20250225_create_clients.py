"""Create clients table

Revision ID: 20250225_create_clients
Revises: 20250216_create_answers
Create Date: 2025-02-25 12:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

revision = '20250225_create_clients'
down_revision = '20250216_create_answers'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'clients',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('vk_id', sa.Integer, unique=True, index=True, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'))
    )

def downgrade():
    op.drop_table('clients')
