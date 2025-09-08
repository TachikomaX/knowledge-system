# -*- coding: utf-8 -*-
# @Time        : 2025-08-28 17:30:14
# @Author      : gaochenyang
# @File        : note.py
# @Description : 2001=创建失败，2002=更新失败，2003=删除失败

# here put the import lib
from fastapi import APIRouter, Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app import crud
from app.auth import get_current_user
from app.db import get_db
from app.models import user as user_model
from app.schemas import NoteCreate, NoteUpdate
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


@router.put("/{note_id}", response_model=dict)
def update_note(
        note_id: int,
        note_data: NoteUpdate,
        db: Session = Depends(get_db),
        current_user: user_model.User = Depends(get_current_user),
):
    note, err = crud.update_note(db,
                                 note_id=note_id,
                                 user_id=current_user.id,
                                 note_update=note_data)
    if err:
        return error_response(code=2002, msg=err)
    return success_response(
        data={
            "id": note.id,
            "title": note.title,
            "content": note.content,
            "summary": note.summary,
            "user_id": note.user_id,
        },
        msg="Note updated successfully",
    )


@router.delete("/{note_id}", response_model=dict)
def delete_note(
        note_id: int,
        db: Session = Depends(get_db),
        current_user: user_model.User = Depends(get_current_user),
):
    ok, err = crud.delete_note(db, note_id=note_id, user_id=current_user.id)
    if not ok:
        return error_response(code=2003, msg=err)
    return success_response(msg="Note deleted successfully")


@router.get("/{note_id}", response_model=dict)
def get_note(
        note_id: int,
        db: Session = Depends(get_db),
        current_user: user_model.User = Depends(get_current_user),
):
    note = crud.get_note(db, note_id=note_id, user_id=current_user.id)
    if not note:
        return error_response(code=2004,
                              msg="Note not found or not authorized")
    return success_response(
        data={
            "id": note.id,
            "title": note.title,
            "content": note.content,
            "summary": note.summary,
            "user_id": note.user_id,
        },
        msg="Note retrieved successfully",
    )


@router.get("", response_model=dict)
def list_notes(
        skip: int = 0,
        limit: int = 20,
        db: Session = Depends(get_db),
        current_user: user_model.User = Depends(get_current_user),
):
    notes = crud.list_notes(db,
                            user_id=current_user.id,
                            skip=skip,
                            limit=limit)
    return success_response(
        data=[{
            "id": note.id,
            "title": note.title,
            "content": note.content,
            "summary": note.summary,
            "user_id": note.user_id,
        } for note in notes],
        msg="Notes retrieved successfully",
    )


# 模糊搜索
@router.get("/search", response_model=dict)
def search_notes(
        q: str,
        skip: int = 0,
        limit: int = 20,
        db: Session = Depends(get_db),
        current_user: user_model.User = Depends(get_current_user),
):
    notes = crud.search_notes(db,
                              user_id=current_user.id,
                              query=q,
                              skip=skip,
                              limit=limit)
    return success_response(
        data=[{
            "id": note.id,
            "title": note.title,
            "content": note.content,
            "summary": note.summary,
            "user_id": note.user_id,
        } for note in notes],
        msg=f"Search results for query '{q}'",
    )
