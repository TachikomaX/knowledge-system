# 用户相关数据库操作
from sqlalchemy.orm import Session

from app.auth import hash_password
from app.models import user as user_model
from app.schemas.user import UserCreate


def get_user_by_email(db: Session, email: str):
    return db.query(
        user_model.User).filter(user_model.User.email == email).first()


def create_user(db: Session, user: UserCreate):
    hashed_pw = hash_password(user.password)
    db_user = user_model.User(username=user.username,
                              email=user.email,
                              hashed_password=hashed_pw)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

