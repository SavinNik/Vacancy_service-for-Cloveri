from uuid import UUID
from datetime import datetime
from pydantic import BaseModel

from app.schemas.base_schemas import RegistryObject


class VacancyData(BaseModel):
    # Основная информация
    title: str
    short_description: str | None | None = None
    requirements: str | None = None
    responsibilities: str | None = None
    benefits: str | None = None
    required_employees: int | None = None

    # Организация
    organization_name: str | None = None
    organization_description: str | None = None

    # Навыки
    skills: list[str] = []

    # Локация
    country: str | None = None
    region: str | None = None
    city: str | None = None

    # Условия работы
    work_format: str | None = None
    employment_type: str | None = None
    employment_basis: str | None = None
    schedule: str | None = None
    experience_required: str | None = None
    education: str | None = None
    experience_level: str | None = None

    # Финансы
    salary_from: float | None = None
    salary_to: float | None = None
    currency: str | None = None
    salary_period: str | None = None
    taxes: bool | None = None

    # Дополнительно
    industry: str | None = None
    vacancy_url: str | None = None
    position: str | None = None
    vacancy_img: str | None = None
    preview_img: str | None = None

    # Контакты
    contact_person_name: str | None = None
    contact_person_phone: str | None = None
    contact_person_email: str | None = None
    contact_person_wa: str | None = None
    contact_person_tg: str | None = None
    opened_date: datetime | None = None
    deadline_date: str | None = None

    recruiter_name: str | None = None
    recruiter_phone: str | None = None
    recruiter_email: str | None = None
    recruiter_wa: str | None = None
    recruiter_tg: str | None = None

    budget_to: float | None = None
    vacancy_status: str | None = None


class VacancyMetaData(BaseModel):
    status: str | None = None
    flags: int | dict | None = None
    internal_id: int | None = None


class VacancyRegistryObject(RegistryObject):
    data: VacancyData | None = None
    meta: VacancyMetaData | None = None

class VacancyDataOptional(VacancyData):
    title: str | None = None


class VacancyUpdateData(BaseModel):
    data: VacancyDataOptional
