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
from app.schemas import (NoteCreate, NoteOut, NoteUpdate, ResponseBase,
                         ResponseWithTotal, SummaryRequest, error_response,
                         success_response, success_response_for_notes)
from app.utils.summary_agent import generate_summary

router = APIRouter(prefix="/api/notes", tags=["notes"])


@router.post("", response_model=ResponseBase[NoteOut])
def create_note(note_data: NoteCreate,
                db: Session = Depends(get_db),
                current_user: user_model.User = Depends(get_current_user)):
    try:
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


@router.post("/generate_summary", response_model=ResponseBase[str])
def regenerate_summary(summary_request: SummaryRequest):
    """生成笔记摘要
    
    可用于新建笔记时生成摘要，或为已有笔记重新生成摘要。
    不依赖数据库中已有的笔记，只需要提供标题和内容即可。
    
    Args:
        summary_request: 包含笔记标题和内容的请求体
    
    Returns:
        生成的摘要文本
    """
    # 调用 AI 摘要生成器
    summary = generate_summary(summary_request.title, summary_request.content)
    if not summary:
        return error_response(code=5001, msg="AI摘要生成失败，请稍后再试")

    return success_response(data=summary, msg="AI摘要生成成功")


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


@router.get("", response_model=ResponseWithTotal[List[NoteOut]])
def list_notes(
        tag_id_list: List[int] = Query([], description="标签 ID 列表"),  # 标签名称
        skip: int = Query(0, ge=0, description="跳过的条数"),
        limit: int = Query(20, ge=1, le=100, description="返回条数限制"),
        db: Session = Depends(get_db),
        current_user: user_model.User = Depends(get_current_user),
):
    if tag_id_list:
        res = crud.get_notes_by_tags(db,
                                     user_id=current_user.id,
                                     tag_id_list=tag_id_list,
                                     skip=skip,
                                     limit=limit)
    else:
        res = crud.list_notes_with_favorites(db,
                                             user_id=current_user.id,
                                             skip=skip,
                                             limit=limit)
    return success_response_for_notes(data=res.get('notes', []),
                                      msg="Notes retrieved successfully",
                                      total=res.get('total', 0))
