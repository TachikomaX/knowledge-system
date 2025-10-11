# -*- coding: utf-8 -*-
# @Time        : 2025-08-20 11:15:26
# @Author      : gaochenyang
# @File        : schemas.py
# @Description :

# here put the import lib
from datetime import datetime
from typing import Generic, List, Optional, TypeVar

from pydantic import BaseModel, EmailStr
from pydantic.generics import GenericModel

T = TypeVar("T")


class ResponseBase(GenericModel, Generic[T]):
    code: int
    msg: str
    data: Optional[T] = None

    class Config:
        orm_mode = True


class ResponseWithTotal(ResponseBase[T]):
    total: Optional[int] = None


# 标准 OAuth2 响应模型
class OAuth2Response(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserBase(BaseModel):
    email: EmailStr
    username: str


class UserCreate(UserBase):
    password: str


class UserOut(UserBase):
    id: int

    class Config:
        orm_mode = True


class TagBase(BaseModel):
    name: str


class TagCreate(TagBase):
    pass


class TagUpdate(BaseModel):
    name: str


class TagOut(TagBase):
    id: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


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


class UserLogin(BaseModel):
    email: EmailStr
    password: str
