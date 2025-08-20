# -*- coding: utf-8 -*-
# @Time        : 2025-08-20 11:15:26
# @Author      : gaochenyang
# @File        : schemas.py
# @Description :

# here put the import lib
from pydantic import BaseModel, EmailStr


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
