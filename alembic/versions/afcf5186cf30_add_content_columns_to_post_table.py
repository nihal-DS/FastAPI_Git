"""add content columns to post table

Revision ID: afcf5186cf30
Revises: 5bfaaa296ad5
Create Date: 2023-05-28 03:18:52.972560

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'afcf5186cf30'
down_revision = '5bfaaa296ad5'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts",
                  sa.Column("content", sa.String(), nullable = True))


def downgrade() -> None:
    op.drop_column("posts", "content")
