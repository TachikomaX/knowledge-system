# -*- coding: utf-8 -*-
# @Time        : 2025-08-28 17:30:14
# @Author      : gaochenyang
# @File        : note.py
# @Description : 2001=创建失败，2002=更新失败，2003=删除失败

# here put the import lib
from typing import List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app import crud
from app.auth import get_current_user
from app.db import get_db
from app.models import user as user_model
from app.schemas import NoteCreate, NoteOut, NoteUpdate, ResponseBase
from app.utils.response import error_response, success_response

router = APIRouter(prefix="/api/notes", tags=["notes"])


@router.post("", response_model=ResponseBase[NoteOut])
def create_note(note_data: NoteCreate,
                db: Session = Depends(get_db),
                current_user: user_model.User = Depends(get_current_user)):
    try:
        # todo 调用AI生成摘要
        note_data.summary = "summary from AI"
        note = crud.create_note(db, user_id=current_user.id, note=note_data)
        return success_response(data=note, msg="Note created successfully")
    except SQLAlchemyError:
        db.rollback()
        return error_response(code=2001, msg="Failed to create note")


@router.put("/{note_id}", response_model=ResponseBase[NoteOut])
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
        data=note,
        msg="Note updated successfully",
    )


@router.delete("/{note_id}", response_model=ResponseBase[None])
def delete_note(
        note_id: int,
        db: Session = Depends(get_db),
        current_user: user_model.User = Depends(get_current_user),
):
    ok, err = crud.delete_note(db, note_id=note_id, user_id=current_user.id)
    if not ok:
        return error_response(code=2003, msg=err)
    return success_response(msg="Note deleted successfully")


# 模糊搜索 基于PostgreSQL 的 全文搜索 (Full-Text Search, FTS)
# FastAPI 是 按路由声明顺序匹配的；/search 的定义要放在 / {note_id} 前面
@router.get("/search", response_model=ResponseBase[List[NoteOut]])
def search_notes(
        q: str = Query(..., description="搜索关键词"),  # 必填
        skip: int = Query(0, ge=0, description="跳过的条数"),
        limit: int = Query(20, ge=1, le=100, description="返回条数限制"),
        db: Session = Depends(get_db),
        current_user: user_model.User = Depends(get_current_user),
):
    try:
        notes = crud.search_notes(db,
                                  user_id=current_user.id,
                                  query=q,
                                  skip=skip,
                                  limit=limit)
        return success_response(msg="success", data=notes)
    except SQLAlchemyError:
        db.rollback()
        return error_response(code=2003, msg="Failed to search notes")


@router.get("/{note_id}", response_model=ResponseBase[NoteOut])
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
        data=note,
        msg="Note retrieved successfully",
    )


@router.get("", response_model=ResponseBase[List[NoteOut]])
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
        data=notes,
        msg="Notes retrieved successfully",
    )
