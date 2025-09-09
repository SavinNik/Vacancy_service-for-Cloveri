from pydantic import BaseModel, Field


class ResponseDetail(BaseModel):
    code: str | None = None
    message: str | None = None


class SuccessfulResponse(BaseModel):
    detail: ResponseDetail
    data: list | None = Field(default=None, examples=[[{}]])


