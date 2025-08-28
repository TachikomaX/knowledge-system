# -*- coding: utf-8 -*-
# @Time        : 2025-08-28 18:26:51
# @Author      : gaochenyang
# @File        : response.py
# @Description :

from typing import Any
from app.schemas import ResponseModel


def success_response(data: Any = None, msg: str = "Success") -> dict:
    return ResponseModel(code=0, msg=msg, data=data).dict()


def error_response(code: int = 1, msg: str = "Error") -> dict:
    return ResponseModel(code=code, msg=msg, data=None).dict()
