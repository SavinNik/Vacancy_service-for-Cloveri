from uuid import uuid4, UUID
from app.schemas.link_schemas import VacancySkillLinkRegistryObject, VacancySkillData
from app.exceptions.main_exceptions import BadRequestException
import logging

logger = logging.getLogger(__name__)

def serialize_vacancy_skill_data_to_registry_object(
        project_id: UUID,
        vacancy_id: UUID,
        skill_id: UUID
) -> VacancySkillLinkRegistryObject:
    """
    Сериализует данные для создания навыка в формат объекта реестра.
    """
    try:
        if not isinstance(project_id, UUID):
            raise BadRequestException(
                code="INVALID_PROJECT_ID",
                message=f"Неверный тип данных для project_id: ожидается UUID, получен {type(project_id)}"
            )
        if not isinstance(vacancy_id, UUID):
            raise BadRequestException(
                code="INVALID_VACANCY_ID",
                message=f"Неверный тип данных для vacancy_id: ожидается UUID, получен {type(vacancy_id)}"
            )
        if not isinstance(skill_id, UUID):
            raise BadRequestException(
                code="INVALID_SKILL_ID",
                message=f"Неверный тип данных для skill_id: ожидается UUID, получен {type(skill_id)}"
            )

        data = VacancySkillData()

        output_data = {
            "id": uuid4(),
            "link_type": "vacancy_skill",
            "link_code": str(uuid4()),
            "project_id": project_id,
            "object1": vacancy_id,
            "object2": skill_id,
            "data": data
        }
        return VacancySkillLinkRegistryObject(**output_data)
    except BadRequestException:
        raise
    except Exception as e:
        error_msg = f"Ошибка при сериализации данных связи вакансии {vacancy_id} с навыком {skill_id}: {str(e)}"
        logger.error(error_msg, exc_info=True)
        raise BadRequestException(
            code="LINK_SERIALIZATION_ERROR",
            message=error_msg
        ) from e
