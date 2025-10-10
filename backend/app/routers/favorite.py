from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, models
from app.auth import get_current_user  # 和你现有保持一致
from app.db import get_db
from app.schemas import NoteOut, ResponseBase
from app.utils.response import error_response, success_response

router = APIRouter(
    prefix="/api/favorites",
    tags=["favorites"],
)


# 收藏笔记
@router.post("/{note_id}", response_model=ResponseBase[dict])
def add_favorite(
        note_id: int,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_user),
):
    favorite, err = crud.add_favorite(db,
                                      user_id=current_user.id,
                                      note_id=note_id)
    if err:
        return error_response(code=3001, msg=err)
    return success_response(data={"note_id": note_id},
                            msg="Note favorited successfully")


# 取消收藏
@router.delete("/{note_id}", response_model=ResponseBase[dict])
def remove_favorite(
        note_id: int,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_user),
):
    success, err = crud.remove_favorite(db,
                                        user_id=current_user.id,
                                        note_id=note_id)
    if err:
        return error_response(code=3002, msg=err)
    return success_response(data={"note_id": note_id},
                            msg="Note unfavorited successfully")


# 获取当前用户的收藏笔记列表
@router.get("", response_model=ResponseBase[List[NoteOut]])
def get_user_favorite_notes(
        skip: int = 0,
        limit: int = 20,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_user),
):
    favorites_notes = crud.get_user_favorite_notes(db,
                                                   user_id=current_user.id,
                                                   skip=skip,
                                                   limit=limit)
    return success_response(data=favorites_notes,
                            msg="Fetched user favorites successfully")


# 判断某笔记是否被收藏
@router.get("/{note_id}/status", response_model=ResponseBase[dict])
def check_favorite_status(
        note_id: int,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_user),
):
    is_favorited = crud.is_note_favorited(db,
                                          user_id=current_user.id,
                                          note_id=note_id)
    return success_response(data={
        "note_id": note_id,
        "is_favorited": is_favorited
    })
