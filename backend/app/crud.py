# -*- coding: utf-8 -*-
# @Time        : 2025-08-20 11:23:59
# @Author      : gaochenyang
# @File        : crud.py
# @Description :

from sqlalchemy import func
# here put the import lib
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

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
    return db_note


def update_note(db: Session, note_id: int, user_id: int,
                note_update: schemas.NoteUpdate):
    note = db.query(models.Note).filter(models.Note.id == note_id).first()
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
    note = db.query(models.Note).filter(
        models.Note.id == note_id, models.Note.user_id == user_id).first()
    return note


# 获取当前用户的所有笔记
def list_notes(db: Session, user_id: int, skip: int = 0, limit: int = 20):
    return db.query(models.Note).filter(
        models.Note.user_id == user_id).offset(skip).limit(limit).all()


# 简单全文搜索
def search_notes(db: Session,
                 user_id: int,
                 query: str,
                 skip: int = 0,
                 limit: int = 20):
    return db.query(models.Note).filter(
        models.Note.user_id == user_id,
        func.to_tsvector(
            'english', models.Note.title + ' ' + models.Note.content + ' ' +
            func.coalesce(models.Note.summary, '')).op('@@')(
                func.plainto_tsquery('english',
                                     query))).offset(skip).limit(limit).all()


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
