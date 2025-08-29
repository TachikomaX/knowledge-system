# -*- coding: utf-8 -*-
# @Time        : 2025-08-29 12:59:48
# @Author      : gaochenyang
# @File        : token.py
# @Description :

# here put the import lib

from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import crud
from app.auth import create_access_token, verify_password
from app.db import get_db
from app.schemas import OAuth2Response

router = APIRouter(prefix="/token", tags=["token"])


@router.post("", response_model=OAuth2Response)
def token(form_data: OAuth2PasswordRequestForm = Depends(),
          db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=form_data.username)

    if not db_user or not verify_password(form_data.password,
                                          db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=30)  # todo 待配置化
    access_token = create_access_token(data={"sub": str(db_user.id)},
                                       expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}
