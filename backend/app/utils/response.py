from typing import Optional

from app.schemas import ResponseBase, T


def success_response(data: Optional[T] = None,
                     msg: str = "success") -> ResponseBase[T]:
    return ResponseBase[T](code=0, msg=msg, data=data)


def error_response(code: int = 1, msg: str = "Error") -> dict:
    return ResponseBase(code=code, msg=msg, data=None).dict()
