# Tag 相关 schema
from pydantic import BaseModel


class TagBase(BaseModel):
    name: str


class TagCreate(TagBase):
    pass


class TagUpdate(BaseModel):
    name: str


class TagOut(TagBase):
    id: int

    class Config:
        orm_mode = True
