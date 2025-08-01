from pydantic import BaseModel
from app.schemas.base_schemas import RegistryObject


class SkillData(BaseModel):
    title: str


class SkillRegistryObject(RegistryObject):
    data: SkillData


class SkillUpdateData(BaseModel):
    title: str | None = None