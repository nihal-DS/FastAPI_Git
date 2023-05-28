"""add user table

Revision ID: 84ac103c656e
Revises: afcf5186cf30
Create Date: 2023-05-28 03:23:02.913625

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '84ac103c656e'
down_revision = 'afcf5186cf30'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("users",
                    sa.Column("id", sa.Integer(), nullable = False),
                    sa.Column("email", sa.String(), nullable = False),
                    sa.Column("password", sa.String(), nullable = False),
                    sa.Column("created_at", sa.TIMESTAMP(timezone = True), server_default = sa.text("now()"), nullable = False),
                    sa.PrimaryKeyConstraint("id"),
                    sa.UniqueConstraint("email")
                    )

def downgrade() -> None:
    op.drop_table("users")
