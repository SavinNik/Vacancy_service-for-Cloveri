from uuid import UUID
from pydantic import BaseModel



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

# Схема вакансии для записи в реестр
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
    organization_uuid: str | None = None

    # Навыки
    # skills: list[str] | None = None

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
    salary_from: str | None = None
    salary_to: str | None = None
    currency: str | None = None
    salary_period: str | None = None
    taxes: bool | None = None
    frequency: str | None = None

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
    opened_date: str | None = None
    deadline_date: str | None = None

    recruiter_name: str | None = None
    recruiter_phone: str | None = None
    recruiter_email: str | None = None
    recruiter_wa: str | None = None
    recruiter_tg: str | None = None

    budget_to: str | None = None
    vacancy_status: str | None = None
    responsible: str | None = None


# Схема входных данных вакансии
class VacancyInputData(VacancyData):
    skills: list[str] | None = None


class VacancyMetaData(BaseModel):
    status: str | None = None
    flags: int | dict | None = None
    internal_id: int | None = None


# Объект реестра вакансии
class VacancyRegistryObject(RegistryObject):
    data: VacancyInputData | None = None
    meta: VacancyMetaData | None = None


#=================== Схемы для обновления вакансии ======================
class VacancyDataOptional(VacancyInputData):
    title: str | None = None


class VacancyUpdateData(BaseModel):
    data: VacancyDataOptional
