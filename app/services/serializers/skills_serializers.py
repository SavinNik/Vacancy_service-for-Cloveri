from uuid import uuid4
from app.schemas.skills_schemas import SkillRegistryObject, SkillData


def serialize_skills_data_to_registry_object(data: list | SkillData) -> list[SkillRegistryObject]:
    """
    Сериализатор для преобразования данных вакансии в объект реестра
    """

    skill_registry_objects = []

    for skill in data:
        if isinstance(skill, str):
            skill_data = SkillData(title=skill)
        elif isinstance(skill, dict):
            skill_data = SkillData(**skill)
        elif isinstance(skill, SkillData):
            skill_data = skill
        else:
            raise ValueError(f"Неверный тип данных: {type(skill)}")

        registry_object_id = str(uuid4())

        registry_object = SkillRegistryObject(
            id=registry_object_id,
            object_type='skill',
            object_code=registry_object_id,
            data=skill_data
        )

        skill_registry_objects.append(registry_object)
    return skill_registry_objects
