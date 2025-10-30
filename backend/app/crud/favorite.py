# Favorite 相关数据库操作
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.sql import exists
from sqlalchemy.exc import SQLAlchemyError
from app import models


# 添加收藏
def add_favorite(db: Session, user_id: int, note_id: int):
    note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if not note:
        return None, "Note not found"

    # 检查是否已收藏
    existing = db.query(models.Favorite).filter_by(user_id=user_id,
                                                   note_id=note_id).first()
    if existing:
        return None, "Already favorited"

    try:
        favorite = models.Favorite(user_id=user_id, note_id=note_id)
        db.add(favorite)
        db.commit()
        db.refresh(favorite)
        return favorite, None
    except SQLAlchemyError as e:
        db.rollback()
        return None, str(e)


# 取消收藏
def remove_favorite(db: Session, user_id: int, note_id: int):
    favorite = db.query(models.Favorite).filter_by(user_id=user_id,
                                                   note_id=note_id).first()
    if not favorite:
        return None, "Not favorited"

    try:
        db.delete(favorite)
        db.commit()
        return True, None
    except SQLAlchemyError as e:
        db.rollback()
        return None, str(e)


# 获取用户收藏列表
def get_user_favorite_notes(db: Session,
                            user_id: int,
                            skip: int = 0,
                            limit: int = 20):
    # 查询收藏总记录数
    total = (db.query(models.Note).join(
        models.Favorite, models.Note.id == models.Favorite.note_id).filter(
            models.Favorite.user_id == user_id).count())
    # 查询当前用户收藏的所有笔记，并支持分页
    res = (
        db.query(models.Note).join(
            models.Favorite, models.Note.id == models.Favorite.note_id).filter(
                models.Favorite.user_id == user_id).options(
                    joinedload(models.Note.tags))  # 预加载 tags
        .order_by(models.Favorite.created_at.desc())  # 按收藏时间降序
        .offset(skip).limit(limit).all())

    for note in res:
        note.is_favorited = True  # 用户的收藏列表，全部标记为已收藏

    return {"total": total, "notes": res}


# 判断某笔记是否被用户收藏
def is_note_favorited(db: Session, user_id: int, note_id: int) -> bool:
    if db.query(models.Favorite).filter_by(user_id=user_id,
                                           note_id=note_id).first():
        return True
    else:
        return False


def list_notes_with_favorites(db: Session,
                              user_id: int,
                              skip: int = 0,
                              limit: int = 20):
    # 查询总记录数
    total = (db.query(
        models.Note).filter(models.Note.user_id == user_id).count())
    # 子查询：判断当前用户是否收藏了笔记
    favorite_subquery = (db.query(models.Favorite.note_id).filter(
        models.Favorite.user_id == user_id).subquery())

    # 主查询：查询笔记并附加 is_favorited 字段
    tmp_notes = (
        db.query(
            models.Note,
            exists().where(
                models.Note.id == favorite_subquery.c.note_id).label(
                    "is_favorited")  # 附加布尔字段
        ).filter(models.Note.user_id == user_id).options(
            joinedload(models.Note.tags))  # 预加载 tags
        .order_by(models.Note.updated_at.desc())  # 按修改时间降序
        .offset(skip).limit(limit).all())

    # 将查询结果中的 is_favorited 字段附加到 Note 对象
    res = []
    for note, is_favorited in tmp_notes:
        note.is_favorited = is_favorited
        res.append(note)

    return {"total": total, "notes": res}
