# 用户相关 schema
from pydantic import BaseModel, ConfigDict, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    username: str
    model_config = ConfigDict(from_attributes=True)


class UserCreate(UserBase):
    password: str


class UserOut(BaseModel):
    id: int
    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    email: EmailStr
    password: str
