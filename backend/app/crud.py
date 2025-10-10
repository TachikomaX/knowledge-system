# -*- coding: utf-8 -*-
# @Time        : 2025-08-20 11:23:59
# @Author      : gaochenyang
# @File        : crud.py
# @Description :

from typing import List

from sqlalchemy import exists, func
# here put the import lib
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, joinedload

from app import auth, models, schemas


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_pw = auth.hash_password(user.password)
    db_user = models.User(username=user.username,
                          email=user.email,
                          hashed_password=hashed_pw)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_note(db: Session, user_id: int, note: schemas.NoteCreate):
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
                note_update: schemas.NoteUpdate):
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


# 简单全文搜索
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
        ).filter(
            models.Note.user_id == user_id,
            func.to_tsvector(
                'english', models.Note.title + ' ' + models.Note.content +
                ' ' + func.coalesce(models.Note.summary, '')).op('@@')(
                    func.plainto_tsquery(
                        'english', query))).offset(skip).limit(limit).all())

    # 将查询结果中的 is_favorited 字段附加到 Note 对象
    res = []
    for note, is_favorited in tmp_notes:
        note.is_favorited = is_favorited
        res.append(note)

    return res


# tag相关
def create_tag(db: Session, user_id: int, tag_in: schemas.TagCreate):
    tag = models.Tag(name=tag_in.name, user_id=user_id)
    db.add(tag)
    db.commit()
    db.refresh(tag)
    return tag


def get_tags(db: Session, user_id: int):
    return db.query(models.Tag).filter(models.Tag.user_id == user_id).all()


def update_tag(db: Session, tag_id: int, user_id: int,
               tag_in: schemas.TagUpdate):
    tag = db.query(models.Tag).filter(models.Tag.id == tag_id,
                                      models.Tag.user_id == user_id).first()
    if tag:
        tag.name = tag_in.name
        db.commit()
        db.refresh(tag)
    return tag


def delete_tag(db: Session, tag_id: int, user_id: int):
    tag = db.query(models.Tag).filter(models.Tag.id == tag_id,
                                      models.Tag.user_id == user_id).first()
    if tag:
        db.delete(tag)
        db.commit()
    return tag


def add_tag_to_note(db: Session, note_id: int, tag_id: int, user_id: int):
    note = db.query(models.Note).filter(
        models.Note.id == note_id, models.Note.user_id == user_id).first()
    tag = db.query(models.Tag).filter(models.Tag.id == tag_id,
                                      models.Tag.user_id == user_id).first()
    if note and tag:
        note.tags.append(tag)
        db.commit()
        db.refresh(note)
    return note


def remove_tag_from_note(db: Session, note_id: int, tag_id: int, user_id: int):
    note = db.query(models.Note).filter(
        models.Note.id == note_id, models.Note.user_id == user_id).first()
    tag = db.query(models.Tag).filter(models.Tag.id == tag_id,
                                      models.Tag.user_id == user_id).first()
    if note and tag and tag in note.tags:
        note.tags.remove(tag)
        db.commit()
        db.refresh(note)
    return note


def get_notes_by_tag_name(db: Session,
                          user_id: int,
                          tag_name: str,
                          skip: int = 0,
                          limit: int = 20):
    try:
        # 子查询优化
        subquery = (db.query(models.Note.id).join(models.Note.tags).filter(
            models.Note.user_id == user_id,
            models.Tag.name == tag_name).offset(skip).limit(limit).subquery())

        # 主查询
        notes = (
            db.query(models.Note).filter(models.Note.id.in_(subquery)).options(
                joinedload(models.Note.tags))  # 预加载 tags
            .all())
        return notes
    except SQLAlchemyError as e:
        raise e


def get_notes_by_tags(db: Session,
                      user_id: int,
                      tag_id_list: List[int],
                      skip: int = 0,
                      limit: int = 20):
    try:
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
            .all())

        # 将查询结果中的 is_favorited 字段附加到 Note 对象
        res = []
        for note, is_favorited in tmp_notes:
            note.is_favorited = is_favorited
            res.append(note)

        return res
    except SQLAlchemyError as e:
        raise e


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
    # 查询当前用户收藏的所有笔记，并支持分页和排序
    res = (
        db.query(models.Note).join(
            models.Favorite, models.Note.id == models.Favorite.note_id).filter(
                models.Favorite.user_id == user_id).options(
                    joinedload(models.Note.tags))  # 预加载 tags
        .order_by(models.Favorite.created_at.desc())  # 按收藏时间降序
        .offset(skip).limit(limit).all())

    for note in res:
        note.is_favorited = True  # 用户的收藏列表，全部标记为已收藏

    return res


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
        .offset(skip).limit(limit).all())

    # 将查询结果中的 is_favorited 字段附加到 Note 对象
    res = []
    for note, is_favorited in tmp_notes:
        note.is_favorited = is_favorited
        res.append(note)

    return res
