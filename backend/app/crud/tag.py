# Tag 相关数据库操作
from sqlalchemy.orm import Session
from app import models
from app.schemas import TagCreate, TagUpdate


# tag相关
def create_tag(db: Session, user_id: int, tag_in: TagCreate):
    tag = models.Tag(name=tag_in.name, user_id=user_id)
    db.add(tag)
    db.commit()
    db.refresh(tag)
    return tag


def get_tags(db: Session, user_id: int):
    return db.query(models.Tag).filter(models.Tag.user_id == user_id).all()


def update_tag(db: Session, tag_id: int, user_id: int, tag_in: TagUpdate):
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
