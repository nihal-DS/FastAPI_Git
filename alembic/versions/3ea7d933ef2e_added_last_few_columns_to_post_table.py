"""added last few columns to post table

Revision ID: 3ea7d933ef2e
Revises: 8bac8deb98b7
Create Date: 2023-05-28 03:38:18.901728

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3ea7d933ef2e'
down_revision = '8bac8deb98b7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts",
                  sa.Column("published", sa.Boolean(), nullable = False, server_default = "True"))
    op.add_column("posts",
                  sa.Column("created_at", sa.TIMESTAMP(timezone = True), nullable = False, server_default = sa.text("NOW()")))

def downgrade() -> None:
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
