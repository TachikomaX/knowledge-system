# -*- coding: utf-8 -*-
# @Time        : 2025-08-28 17:30:14
# @Author      : gaochenyang
# @File        : note.py
# @Description :

# here put the import lib
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import user as user_model
from app.auth import hash_password, verify_password, create_access_token, get_current_user
from datetime import timedelta

router = APIRouter(prefix="/notes", tags=["notes"])


@router.post("")
def create_note(title: str,
                content: str,
                summary: str,
                current_user: user_model.User = Depends(get_current_user)):
    # todo 校验登录态
    # # 检查邮箱是否已注册
    # existing_user = db.query(
    #     user_model.User).filter(user_model.User.email == email).first()
    # if existing_user:
    #     raise HTTPException(status_code=400, detail="Email already registered")

    # hashed_pw = hash_password(password)
    # new_user = user_model.User(username=username,
    #                            email=email,
    #                            hashed_password=hashed_pw)
    # db.add(new_user)
    # db.commit()
    # db.refresh(new_user)
    return {
        "code": 0,
        "msg": "sucess",
    }
