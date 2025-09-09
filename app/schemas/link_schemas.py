from pydantic import BaseModel
from uuid import UUID


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
    meta: dict | None = None


class VacancySkillData(BaseModel):
    requirement_type: str | None = None
    experience_required: str | None = None


class VacancySkillLinkRegistryObject(BaseModel):
    id: UUID | None = None
    link_type: str | None = None
    link_code: str | None = None
    object1: UUID | None = None
    object2: UUID | None = None
    weight: float | None = None
    direction: int | None = None
    data: VacancySkillData | None = None
    project_id: UUID | None = None
    account_id: UUID | None = None
    user_id: UUID | None = None
    meta: dict | None = None




