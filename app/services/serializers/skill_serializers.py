from uuid import uuid4, UUID
from app.schemas.skills_schemas import SkillData, SkillRegistryObject
from app.exceptions.main_exceptions import BadRequestException
import logging

logger = logging.getLogger(__name__)


def serialize_skill_data_to_registry_object(
        skill_name: str,
        project_id: UUID
) -> SkillRegistryObject:
    """
    Сериализует данные для создания навыка в формат объекта реестра.
    """
    try:
        if not isinstance(skill_name, str):
            raise BadRequestException(
                code="INVALID_SKILL_INPUT",
                message=f"Неверный тип данных для названия навыка: ожидается str, получен {type(skill_name)}"
            )
        if not isinstance(project_id, UUID):
            raise BadRequestException(
                code="INVALID_PROJECT_ID",
                message=f"Неверный тип данных для project_id: ожидается UUID, получен {type(project_id)}"
            )

        data = SkillData(title=skill_name)

        output_data = {
            "id": uuid4(),
            "object_type": "skill",
            "project_id": project_id,
            "data": data
        }
        return SkillRegistryObject(**output_data)

    except BadRequestException:
        raise
    except Exception as e:
        error_msg = f"Ошибка при сериализации данных навыка '{skill_name}': {str(e)}"
        logger.error(error_msg, exc_info=True)
        raise BadRequestException(
            code="SKILL_SERIALIZATION_ERROR",
            message=error_msg
        ) from e