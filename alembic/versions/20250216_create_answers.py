"""create answers table

Revision ID: 20230210_create_answers
Revises:
Create Date: 2023-02-10

"""
from alembic import op
import sqlalchemy as sa


# Идентификатор ревизии
revision = '20250216_create_answers'
down_revision = None  # или укажите предыдущую ревизию, если есть
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'answers',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('key', sa.String(100), nullable=False, unique=True),
        sa.Column('description', sa.String(255), nullable=True),
        sa.Column('message', sa.String(4096), nullable=True),  # до 4096 символов
        sa.Column('can_change', sa.Boolean, nullable=False, server_default='false'),
    )


def downgrade():
    op.drop_table('answers')
