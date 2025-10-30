# Note 相关数据库操作
from typing import List

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.sql import exists

from app import models
# 如果 is_note_favorited 是本模块外部函数，需要导入
from app.crud.favorite import is_note_favorited
from app.schemas import NoteCreate, NoteUpdate


def create_note(db: Session, user_id: int, note: NoteCreate):
    db_note = models.Note(
        user_id=user_id,
        title=note.title,
        content=note.content,
        summary=note.summary,
    )

    # 处理 tags（只允许已有标签）
    if note.tags:
        tags = []
        for tag_id in note.tags:
            tag = db.query(models.Tag).filter(models.Tag.id == tag_id).first()
            if not tag:
                raise ValueError(f"Tag '{tag_id}' does not exist")  # 阻止新建
            tags.append(tag)
        db_note.tags = tags

    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    db_note.is_favorited = False  # 新建的笔记默认未收藏
    return db_note


def update_note(db: Session, note_id: int, user_id: int,
                note_update: NoteUpdate):
    note = db.query(models.Note).filter(models.Note.id == note_id).first()
    # 判断是否被收藏
    note.is_favorited = is_note_favorited(db, user_id, note_id)
    if not note:
        return None, "Note not found"
    if note.user_id != user_id:
        return None, "Not authorized to edit this note"

    if note_update.title is not None:
        note.title = note_update.title
    if note_update.content is not None:
        note.content = note_update.content
    if note_update.summary is not None:
        note.summary = note_update.summary

    # 更新 tags（如果传了就整体替换，并严格校验存在性）
    if note_update.tags is not None:
        tags = []
        for tag_id in note_update.tags:
            tag = db.query(models.Tag).filter(models.Tag.id == tag_id).first()
            if not tag:
                return None, f"Tag '{tag_id}' does not exist"
            tags.append(tag)
        note.tags = tags
    try:
        db.commit()
        db.refresh(note)
        return note, None
    except SQLAlchemyError as e:
        db.rollback()
        return None, str(e)


def delete_note(db: Session, note_id: int, user_id: int):
    note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if not note:
        return False, "Note not found"
    if note.user_id != user_id:
        return False, "Not authorized to delete this note"

    try:
        db.delete(note)
        db.commit()
        return True, None
    except SQLAlchemyError as e:
        db.rollback()
        return False, str(e)


# 获取单个笔记
def get_note(db: Session, note_id: int, user_id: int):
    # 查询单个笔记
    note = (
        db.query(models.Note).filter(
            models.Note.id == note_id, models.Note.user_id == user_id).options(
                joinedload(models.Note.tags))  # 预加载 tags
        .first())

    if not note:
        return None

    # 判断是否被收藏
    note.is_favorited = is_note_favorited(db, user_id, note_id)

    return note


# 简单全文搜索 todo 接入ElasticSearch？
def search_notes(db: Session,
                 user_id: int,
                 query: str,
                 skip: int = 0,
                 limit: int = 20):
    # 子查询：判断当前用户是否收藏了笔记
    favorite_subquery = (db.query(models.Favorite.note_id).filter(
        models.Favorite.user_id == user_id).subquery())

    # 主查询：全文搜索笔记，并附加 is_favorited 字段
    tmp_notes = (
        db.query(
            models.Note,
            exists().where(
                models.Note.id == favorite_subquery.c.note_id).label(
                    "is_favorited")  # 附加布尔字段
        ).filter(models.Note.user_id == user_id,
                 (models.Note.title.ilike(f"%{query}%")
                  | models.Note.content.ilike(f"%{query}%")
                  | models.Note.summary.ilike(f"%{query}%")
                  )).offset(skip).limit(limit).all())

    # 将查询结果中的 is_favorited 字段附加到 Note 对象
    res = []
    for note, is_favorited in tmp_notes:
        note.is_favorited = is_favorited
        res.append(note)

    return res


def get_notes_by_tags(db: Session,
                      user_id: int,
                      tag_id_list: List[int],
                      skip: int = 0,
                      limit: int = 20):
    try:
        # 查询总记录数
        total = (
            db.query(models.Note).join(models.Note.tags)  # 关联 tags 表
            .filter(
                models.Note.user_id == user_id,
                models.Tag.id.in_(tag_id_list)  # 根据 tag_id_list 过滤
            ).group_by(models.Note.id)  # 按笔记分组
            .count())
        # 子查询：判断当前用户是否收藏了笔记
        favorite_subquery = (db.query(models.Favorite.note_id).filter(
            models.Favorite.user_id == user_id).subquery())

        # 子查询：查询符合条件的笔记 ID
        note_subquery = (
            db.query(models.Note.id).join(models.Note.tags)  # 关联 tags 表
            .filter(
                models.Note.user_id == user_id,
                models.Tag.id.in_(tag_id_list)  # 根据 tag_id_list 过滤
            ).group_by(models.Note.id)  # 按笔记分组
            .offset(skip).limit(limit).subquery())

        # 主查询：根据子查询的笔记 ID 获取完整的笔记数据，并附加 is_favorited 字段
        tmp_notes = (
            db.query(
                models.Note,
                exists().where(
                    models.Note.id == favorite_subquery.c.note_id).label(
                        "is_favorited")  # 附加布尔字段
            ).filter(models.Note.id.in_(note_subquery)).options(
                joinedload(models.Note.tags))  # 预加载 tags
            .order_by(models.Note.updated_at.desc())  # 按修改时间降序
            .all())

        # 将查询结果中的 is_favorited 字段附加到 Note 对象
        res = []
        for note, is_favorited in tmp_notes:
            note.is_favorited = is_favorited
            res.append(note)

        return {"total": total, "notes": res}
    except SQLAlchemyError as e:
        raise e
