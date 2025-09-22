"""add user_id to tags

Revision ID: b267a5c15845
Revises: a59deba3aabb
Create Date: 2025-09-12 17:40:27.941409

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'b267a5c15845'
down_revision: Union[str, Sequence[str], None] = 'a59deba3aabb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # 1. 增加 user_id 字段
    op.add_column("tags", sa.Column("user_id", sa.Integer(), nullable=False))

    # 2. 添加外键约束
    op.create_foreign_key(
        "fk_tags_user_id_users",
        "tags",
        "users",
        ["user_id"],
        ["id"],
        ondelete="CASCADE",
    )

    # 3. 添加联合唯一约束 (user_id + name)
    op.create_unique_constraint("uq_user_tag", "tags", ["user_id", "name"])


def downgrade():
    # 回滚操作，按顺序删除约束和列
    op.drop_constraint("uq_user_tag", "tags", type_="unique")
    op.drop_constraint("fk_tags_user_id_users", "tags", type_="foreignkey")
    op.drop_column("tags", "user_id")
