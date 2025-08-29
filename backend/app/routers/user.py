# -*- coding: utf-8 -*-
# @Time        : 2025-08-20 11:22:18
# @Author      : gaochenyang
# @File        : user.py
# @Description :

from datetime import timedelta

from fastapi import APIRouter, Depends
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app import crud
from app.auth import create_access_token, get_current_user, verify_password
from app.db import get_db
from app.models import user as user_model
from app.schemas import UserCreate, UserLogin
from app.utils.response import error_response, success_response

router = APIRouter(prefix="/users", tags=["users"])


# 注册
@router.post("/register", response_model=dict)
def register(user: UserCreate, db: Session = Depends(get_db)):
    try:
        db_user = crud.create_user(db, user)
        return success_response(data={
            "id": db_user.id,
            "username": db_user.username,
            "email": db_user.email
        },
                                msg="User registered successfully")

    except IntegrityError:
        db.rollback()
        return error_response(code=1001,
                              msg="Email or username already registered")

    except SQLAlchemyError:
        db.rollback()
        return error_response(code=1002,
                              msg="Database error, please try again later")


# 登录 应用层封装写法（OAuth2 标准写法）
# fastapi.Depends用于声明和注入依赖项到路由处理函数中，
# 以便处理函数可以使用这些依赖项来获取数据、执行验证、进行身份认证等操作
# OAuth2 规范明确要求 token 请求必须使用 application/x-www-form-urlencoded，而不是 application/json。
@router.post("/login", response_model=dict)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if not db_user or not verify_password(user.password,
                                          db_user.hashed_password):
        return error_response(code=1003, msg="Incorrect email or password")

    access_token_expires = timedelta(minutes=30)  # todo 待配置化
    access_token = create_access_token(data={"sub": str(db_user.id)},
                                       expires_delta=access_token_expires)

    return success_response(data={
        "access_token": access_token,
        "token_type": "bearer"
    },
                            msg="Login successful")


# 获取当前登录用户
@router.get("/me", response_model=dict)
def get_me(current_user: user_model.User = Depends(get_current_user)):
    return success_response(data={
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "created_at": current_user.created_at,
    },
                            msg="User info retrieved successfully")
