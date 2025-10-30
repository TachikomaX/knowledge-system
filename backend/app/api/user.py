# -*- coding: utf-8 -*-
# @Time        : 2025-08-20 11:22:18
# @Author      : gaochenyang
# @File        : user.py
# @Description :

from fastapi import APIRouter, Depends
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app import crud
from app.auth import create_access_token, get_current_user, verify_password
from app.db import get_db
from app.models import user as user_model
from app.schemas import (OAuth2Response, ResponseBase, UserCreate, UserLogin,
                         UserOut, error_response, success_response)

router = APIRouter(prefix="/api/users", tags=["users"])


# 注册
@router.post("/register", response_model=ResponseBase[UserOut])
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    try:
        # 先检查用户名
        if db.query(user_model.User).filter(
                user_model.User.username == user_data.username).first():
            return error_response(code=1001, msg="Username already registered")

        # 再检查邮箱
        if db.query(user_model.User).filter(
                user_model.User.email == user_data.email).first():
            return error_response(code=1002, msg="Email already registered")

        # 尝试创建用户
        user = crud.create_user(db, user_data)
        return success_response(data=user, msg="User registered successfully")

    except IntegrityError:
        # 并发下可能漏网 —— 再兜底
        db.rollback()
        return error_response(code=1003,
                              msg="Email or username already registered")

    except SQLAlchemyError:
        db.rollback()
        return error_response(code=1004,
                              msg="Database error, please try again later")


# 登录 应用层封装写法（OAuth2 标准写法）
# fastapi.Depends用于声明和注入依赖项到路由处理函数中，
# 以便处理函数可以使用这些依赖项来获取数据、执行验证、进行身份认证等操作
# OAuth2 规范明确要求 token 请求必须使用 application/x-www-form-urlencoded，而不是 application/json。
@router.post("/login", response_model=ResponseBase[OAuth2Response])
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if not db_user or not verify_password(user.password,
                                          db_user.hashed_password):
        return error_response(code=1003, msg="Incorrect email or password")

    access_token = create_access_token(data={"sub": str(db_user.id)})

    return success_response(data={
        "access_token": access_token,
        "token_type": "bearer"
    },
                            msg="Login successful")


# 获取当前登录用户
@router.get("/me", response_model=ResponseBase[UserOut])
def get_me(current_user: user_model.User = Depends(get_current_user)):
    return success_response(data=current_user,
                            msg="User info retrieved successfully")
