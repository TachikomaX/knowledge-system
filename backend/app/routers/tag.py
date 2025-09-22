# -*- coding: utf-8 -*-
# @Time        : 2025-09-11 18:46:56
# @Author      : gaochenyang
# @File        : tag.py
# @Description :

# routers/tags.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import crud, models
from app.db import get_db
from app.auth import get_current_user
from app.schemas import TagOut, ResponseBase, TagCreate, TagUpdate

router = APIRouter(prefix="/tags", tags=["tags"])


@router.post("", response_model=ResponseBase[TagOut])
def create_tag(
        tag_in: TagCreate,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_user),
):
    tag = crud.create_tag(db, current_user.id, tag_in)
    return ResponseBase(code=0, msg="Tag created successfully", data=tag)


@router.get("", response_model=ResponseBase[List[TagOut]])
def get_tags(
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_user),
):
    tags = crud.get_tags(db, current_user.id)
    return ResponseBase(code=0, msg="Tags retrieved successfully", data=tags)


@router.put("/{tag_id}", response_model=ResponseBase[TagOut])
def update_tag(
        tag_id: int,
        tag_in: TagUpdate,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_user),
):
    tag = crud.update_tag(db, tag_id, current_user.id, tag_in)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return ResponseBase(code=0, msg="Tag updated successfully", data=tag)


@router.delete("/{tag_id}", response_model=ResponseBase[dict])
def delete_tag(
        tag_id: int,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_user),
):
    tag = crud.delete_tag(db, tag_id, current_user.id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return ResponseBase(code=0,
                        msg="Tag deleted successfully",
                        data={"id": tag_id})


# === Note 与 Tag 关系接口 ===
@router.post("/{tag_id}/notes/{note_id}", response_model=ResponseBase[dict])
def add_tag_to_note(
        tag_id: int,
        note_id: int,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_user),
):
    note = crud.add_tag_to_note(db, note_id, tag_id, current_user.id)
    if not note:
        raise HTTPException(status_code=404, detail="Note or Tag not found")
    return ResponseBase(code=0,
                        msg="Tag added to note successfully",
                        data={
                            "note_id": note_id,
                            "tag_id": tag_id
                        })


@router.delete("/{tag_id}/notes/{note_id}", response_model=ResponseBase[dict])
def remove_tag_from_note(
        tag_id: int,
        note_id: int,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_user),
):
    note = crud.remove_tag_from_note(db, note_id, tag_id, current_user.id)
    if not note:
        raise HTTPException(status_code=404, detail="Note or Tag not found")
    return ResponseBase(code=0,
                        msg="Tag removed from note successfully",
                        data={
                            "note_id": note_id,
                            "tag_id": tag_id
                        })
