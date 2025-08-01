from pydantic import BaseModel
from app.schemas.base_schemas import LinkObject
from uuid import UUID


class VacancySkillData(BaseModel):
    requirement_type: str | None = None
    experience_required: str | None = None


class VacancySkillLink(LinkObject):
    data: VacancySkillData


class VacancySkillLinkInputData(BaseModel):
    link_id: UUID | None = None
    vacancy_id: UUID
    skill_id: UUID
    link_weight: float | None = 0
    project_id: UUID | None
