# -*- coding: utf-8 -*-
# @Time        : 2025-08-20 11:22:18
# @Author      : gaochenyang
# @File        : user.py
# @Description :

# here put the import lib
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import user as user_model
from app.auth import hash_password, verify_password, create_access_token, get_current_user
from datetime import timedelta

router = APIRouter(prefix="/users", tags=["users"])


# 注册新用户
@router.post("/register", response_model=dict)
def register(username: str,
             email: str,
             password: str,
             db: Session = Depends(get_db)):
    # 检查邮箱是否已注册
    existing_user = db.query(
        user_model.User).filter(user_model.User.email == email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = hash_password(password)
    new_user = user_model.User(username=username,
                               email=email,
                               hashed_password=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"msg": "User registered successfully"}


# 登录（OAuth2 标准写法）
# fastapi.Depends用于声明和注入依赖项到路由处理函数中，
# 以便处理函数可以使用这些依赖项来获取数据、执行验证、进行身份认证等操作
@router.post("/login", response_model=dict)
def login(form_data: OAuth2PasswordRequestForm = Depends(),
          db: Session = Depends(get_db)):
    # OAuth2PasswordRequestForm.username 实际存放 email
    user = db.query(user_model.User).filter(
        user_model.User.email == form_data.username).first()
    if not user or not verify_password(form_data.password,
                                       user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect email or password")

    access_token_expires = timedelta(minutes=30)  # todo 过期时间配置化
    token = create_access_token(data={"sub": user.email},
                                expires_delta=access_token_expires)

    return {"access_token": token, "token_type": "bearer"}


# 获取当前登录用户
@router.get("/me")
def get_me(current_user: user_model.User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "created_at": current_user.created_at,
    }
