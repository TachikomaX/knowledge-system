# Note 相关 schema
from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List

from app.schemas.tag import TagOut


class NoteBase(BaseModel):
    title: str
    content: str
    summary: Optional[str] = None


class NoteCreate(NoteBase):
    tags: Optional[List[int]] = []  # 前端传 tag 的 id 列表


class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    summary: Optional[str] = None
    tags: Optional[List[int]] = []


class NoteOut(NoteBase):
    user_id: int
    id: int
    created_at: datetime
    updated_at: datetime
    tags: List[TagOut] = []
    is_favorited: bool

    class Config:
        orm_mode = True
        from_attributes = True
