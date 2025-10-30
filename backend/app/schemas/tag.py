# Tag 相关 schema
from pydantic import BaseModel, ConfigDict


class TagBase(BaseModel):
    name: str
    model_config = ConfigDict(from_attributes=True)


class TagCreate(TagBase):
    pass


class TagUpdate(BaseModel):
    name: str


class TagOut(TagBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
