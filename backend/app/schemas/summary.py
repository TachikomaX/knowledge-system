from pydantic import BaseModel


class SummaryRequest(BaseModel):
    title: str
    content: str


class SummaryResponse(BaseModel):
    summary: str
