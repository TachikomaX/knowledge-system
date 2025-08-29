# -*- coding: utf-8 -*-
# @Time        : 2025-08-28 17:30:14
# @Author      : gaochenyang
# @File        : note.py
# @Description :

# here put the import lib
from fastapi import APIRouter, Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app import crud
from app.auth import get_current_user
from app.db import get_db
from app.models import user as user_model
from app.schemas import NoteCreate
from app.utils.response import error_response, success_response

router = APIRouter(prefix="/notes", tags=["notes"])


@router.post("", response_model=dict)
def create_note(note: NoteCreate,
                db: Session = Depends(get_db),
                current_user: user_model.User = Depends(get_current_user)):
    try:
        # todo 调用AI生成摘要
        note.summary = "from AI"
        db_note = crud.create_note(db, user_id=current_user.id, note=note)
        return success_response(data={
            "id": db_note.id,
            "title": db_note.title,
            "content": db_note.content,
            "summary": db_note.summary,
            "user_id": db_note.user_id
        },
                                msg="Note created successfully")
    except SQLAlchemyError:
        db.rollback()
        return error_response(code=2001, msg="Failed to create note")
