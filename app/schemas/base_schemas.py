from uuid import UUID

from pydantic import BaseModel


class RegistryDataTitleValue(BaseModel):
    title: str
    value: str


class RegistryObject(BaseModel):
    id: UUID | None = None
    object_type: str | None = None
    name: str | None = None
    object_code: str | None = None
    data: dict | None = None
    meta: dict | None = None
    project_id: UUID | None = None
    account_id: UUID | None = None
    user_id: UUID | None = None
    object_item: UUID | None = None


class LinkObject(BaseModel):
    id: UUID | None = None
    link_type: str | None = None
    link_code: str | None = None
    object1: UUID | None = None
    object2: UUID | None = None
    weight: float | None = None
    direction: int | None = None
    data: dict | None = None
    project_id: UUID | None = None
    account_id: UUID | None = None
    user_id: UUID | None = None
