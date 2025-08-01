from pydantic import BaseModel, Field

from app.config import settings
from app.schemas.base_schemas import RegistryObject


class ResponseDetail(BaseModel):
    code: str | None = None
    message: str | None = None


class ExceptionDetail(BaseModel):
    detail: ResponseDetail


class ResponseInfo(BaseModel):
    api_version: str = settings.VERSION
    count: int = None
    limit: int | None = 50
    offset: int | None = 0

    class Config:
        extra = "allow"


class SuccessfulResponse(BaseModel):
    detail: ResponseDetail
    data: list | None = Field(default=None, examples=[[{}]])
    info: ResponseInfo


