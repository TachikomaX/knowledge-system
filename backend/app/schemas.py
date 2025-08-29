# -*- coding: utf-8 -*-
# @Time        : 2025-08-20 11:15:26
# @Author      : gaochenyang
# @File        : schemas.py
# @Description :

# here put the import lib
from typing import Any, Optional

from pydantic import BaseModel, EmailStr


class ResponseModel(BaseModel):
    code: int
    msg: str
    data: Optional[Any] = None


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


class Token(BaseModel):
    access_token: str
    token_type: str


class NoteBase(BaseModel):
    title: str
    content: str
    summary: str


class NoteCreate(NoteBase):
    pass


class NoteOut(NoteBase):
    user_id: int
    id: int
    created_at: int
    updated_at: int

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str
