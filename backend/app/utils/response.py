from typing import Optional

from app.schemas import ResponseBase, T, ResponseWithTotal


def success_response(data: Optional[T] = None,
                     msg: str = "success") -> ResponseBase[T]:
    return ResponseBase[T](code=0, msg=msg,
                           data=data).model_dump(exclude_none=True)


def success_response_for_notes(data: Optional[T] = None,
                     msg: str = "success",
                     total: int = 0) -> ResponseBase[T]:
    return ResponseWithTotal[T](code=0, msg=msg, data=data,
                                total=total)


def error_response(code: int = 1, msg: str = "Error") -> dict:
    return ResponseBase(code=code, msg=msg, data=None).dict()
