# -*- coding: utf-8 -*-
# @Time        : 2025-08-20 11:23:59
# @Author      : gaochenyang
# @File        : crud.py
# @Description :

from sqlalchemy.exc import IntegrityError, SQLAlchemyError
# here put the import lib
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
    db_note = models.Note(user_id=user_id,
                            title=note.title,
                            content=note.content,
                            summary=note.summary)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

