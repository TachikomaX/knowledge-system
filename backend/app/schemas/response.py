from typing import Generic, TypeVar, Optional
from pydantic import BaseModel, ConfigDict

T = TypeVar("T")


class ResponseBase(BaseModel, Generic[T]):
    code: int
    msg: str
    data: Optional[T] = None
    model_config = ConfigDict(from_attributes=True)


class ResponseWithTotal(ResponseBase[T]):
    total: Optional[int] = None


# 标准 OAuth2 响应模型
class OAuth2Response(BaseModel):
    access_token: str
    token_type: str = "bearer"


def success_response(data: Optional[T] = None,
                     msg: str = "success") -> ResponseBase[T]:
    return ResponseBase[T](code=0, msg=msg,
                           data=data).model_dump(exclude_none=True)


def success_response_for_notes(data: Optional[T] = None,
                               msg: str = "success",
                               total: int = 0) -> ResponseBase[T]:
    return ResponseWithTotal[T](code=0, msg=msg, data=data, total=total)


def error_response(code: int = 1, msg: str = "Error") -> dict:
    return ResponseBase(code=code, msg=msg, data=None).model_dump()
