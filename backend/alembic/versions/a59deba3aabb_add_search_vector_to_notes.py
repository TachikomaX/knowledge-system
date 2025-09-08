"""add search_vector to notes

Revision ID: a59deba3aabb
Revises: dcdcc613d5fc
Create Date: 2025-09-08 12:24:01.269915

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'a59deba3aabb'
down_revision: Union[str, Sequence[str], None] = 'dcdcc613d5fc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # 添加 search_vector 字段
    op.add_column(
        "notes", sa.Column("search_vector", sa.dialects.postgresql.TSVECTOR()))

    # 创建 GIN 索引
    op.execute(
        "CREATE INDEX notes_search_idx ON notes USING GIN (search_vector)")

    # 初始化已有数据的 search_vector
    op.execute(
        "UPDATE notes SET search_vector = to_tsvector('english', coalesce(title,'') || ' ' || coalesce(content,'') || ' ' || coalesce(summary,''))"
    )

    # 触发器：自动更新 search_vector
    op.execute("""
    CREATE FUNCTION notes_search_vector_trigger() RETURNS trigger AS $$
    begin
      new.search_vector :=
         to_tsvector('english', coalesce(new.title,'') || ' ' || coalesce(new.content,'') || ' ' || coalesce(new.summary,''));
      return new;
    end
    $$ LANGUAGE plpgsql;
    """)

    op.execute("""
    CREATE TRIGGER notes_search_vector_update
    BEFORE INSERT OR UPDATE ON notes
    FOR EACH ROW EXECUTE FUNCTION notes_search_vector_trigger();
    """)


def downgrade():
    op.execute("DROP TRIGGER IF EXISTS notes_search_vector_update ON notes")
    op.execute("DROP FUNCTION IF EXISTS notes_search_vector_trigger")
    op.drop_index("notes_search_idx", table_name="notes")
    op.drop_column("notes", "search_vector")
