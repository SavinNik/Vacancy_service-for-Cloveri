from uuid import uuid4, UUID
from app.schemas.vacancy_schemas import VacancyRegistryObject, VacancyData
from app.exceptions.main_exceptions import BadRequestException
import logging

logger = logging.getLogger(__name__)

def serialize_vacancy_data_to_registry_object(
        data: dict,
        project_id: UUID
) -> VacancyRegistryObject:
    """
    Сериализует данные для создания вакансии (POST) в формат объекта реестра.
    """
    try:
        if not isinstance(data, dict):
            raise BadRequestException(
                code="INVALID_VACANCY_INPUT",
                message=f"Неверный тип данных: ожидается dict, получен {type(data)}"
            )

        vacancy_data = VacancyData(**data)

        output_data = {
            "id": uuid4(),
            "object_type": "vacancy",
            "project_id": project_id,
            "data": vacancy_data.model_dump()
        }
        return VacancyRegistryObject(**output_data)


    except BadRequestException:
        raise
    except Exception as e:
        error_msg = f"Ошибка при сериализации данных вакансии: {str(e)}"
        logger.error(error_msg, exc_info=True)
        raise BadRequestException(
            code="SERIALIZATION_ERROR",
            message=error_msg
        ) from e

