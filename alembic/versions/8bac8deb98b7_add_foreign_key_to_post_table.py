"""add foreign key to post table

Revision ID: 8bac8deb98b7
Revises: 84ac103c656e
Create Date: 2023-05-28 03:30:26.271716

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8bac8deb98b7'
down_revision = '84ac103c656e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts",
                  sa.Column("owner_id", sa.Integer(), nullable = False))
    op.create_foreign_key("post_users_fk", source_table = "posts", referent_table = "users",
                          local_cols = ["owner_id"], remote_cols = ["id"], ondelete = "CASCADE")

def downgrade() -> None:
    op.drop_constraint("post_users_fk", table_name = "posts")
    op.drop_column("posts", "owner_id")
    
