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
    user_id: int


class NoteCreate(NoteBase):
    pass


class NoteOut(NoteBase):
    id: int
    created_at: int
    updated_at: int

    class Config:
        orm_mode = True
