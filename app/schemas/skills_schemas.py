from pydantic import BaseModel
from uuid import UUID


class SkillData(BaseModel):
    title: str


class SkillRegistryObject(BaseModel):
    id: UUID | None = None
    object_type: str | None = None
    name: str | None = None
    object_code: str | None = None
    data: SkillData
    meta: dict | None = None
    project_id: UUID | None = None
    account_id: UUID | None = None
    user_id: UUID | None = None
    object_item: UUID | None = None



