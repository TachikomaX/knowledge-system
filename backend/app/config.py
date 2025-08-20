# -*- coding: utf-8 -*-
# @Time        : 2025-08-20 11:12:26
# @Author      : gaochenyang
# @File        : config.py
# @Description :

# here put the import lib
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"  # 指定读取 backend/.env 文件


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
