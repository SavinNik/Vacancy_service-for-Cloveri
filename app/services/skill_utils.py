from uuid import UUID

from app.services.registry_interaction import interact_with_registry
from app.config import settings
from fastapi import Request

from app.services.serializers.link_serializers import serialize_vacancy_skill_data_to_registry_object
from app.services.serializers.skill_serializers import serialize_skill_data_to_registry_object
from app.services.utils import RegistryName, Method

from app.exceptions.main_exceptions import BadRequestException, InternalException
from app.exceptions.sub_exceptions.failed_dependency_exceptions import RegistryInteractionException
import logging


logger = logging.getLogger(__name__)


def get_skills_from_vacancy(vacancy_data: dict) -> list[str]:
    """
    Извлекает и удаляет список навыков из данных вакансии
    """
    try:
        skills = vacancy_data.pop('skills', []) or []
        if not isinstance(skills, list):
            raise BadRequestException(code="INVALID_SKILLS_FORMAT", message=f"Поле 'skills' должно быть списком. Получен тип {type(skills)}.")
        for i, skill in enumerate(skills):
            if not isinstance(skill, str):
                 raise BadRequestException(code="INVALID_SKILL_FORMAT", message=f"Навык под индексом {i} должен быть строкой. Получен тип {type(skill)}.")
        return skills
    except BadRequestException:
        raise
    except Exception as e:
        logger.error(f"Неожиданная ошибка при извлечении навыков из данных вакансии: {e}", exc_info=True)
        raise InternalException(message="Ошибка при обработке навыков вакансии.") from e


async def get_all_skills_from_registry(
        project_id: UUID,
        request: Request
) -> dict:
    """
    Получаем все существующие навыки из реестра навыков по project_id
    """
    params = {'project_id': project_id}
    try:
        existing_skills = await interact_with_registry(
            method=Method.GET,
            request=request,
            registry_url=settings.SKILLS_REGISTRY_URL,
            registry_name=RegistryName.SKILLS,
            params=params
        )
        if not isinstance(existing_skills, list):
            logger.error(f"Ожидался список навыков от реестра, но получен {type(existing_skills)}")
            return {}

        skill_names_and_ids = {}

        for skill in existing_skills:
            if not isinstance(skill, dict):
                continue
            skill_data = skill.get('data', {})
            if not isinstance(skill_data, dict):
                continue
            skill_name = skill_data.get('title')
            if not skill_name or not isinstance(skill_name, str):
                continue
            skill_name_lower = skill_name.lower()
            skill_id = skill.get('id')

            if skill_id:
                skill_names_and_ids[skill_name_lower] = skill_id

        return skill_names_and_ids


    except RegistryInteractionException as e:
        logger.error(f"Ошибка взаимодействия с реестром навыков для project_id {project_id}: {e}", exc_info=True)
        return {}
    except Exception as e:
        logger.error(f"Неожиданная ошибка при получении навыков из реестра для project_id {project_id}: {e}", exc_info=True)
        return {}


async def add_vacancy_skill_to_registry(
        project_id: UUID,
        request: Request,
        skill_name: str,

) -> dict:
    """
    Добавляет новый навык в реестр
    """
    try:
        data_ser = serialize_skill_data_to_registry_object(skill_name=skill_name, project_id=project_id)
        data = data_ser.model_dump(exclude_none=True)

        skill_response = await interact_with_registry(
            method=Method.POST,
            request=request,
            registry_url=settings.SKILLS_REGISTRY_URL,
            registry_name=RegistryName.SKILL,
            data=data
        )
        if not isinstance(skill_response, dict):
            logger.error(f"Ожидался словарь с данными навыка от реестра, но получен {type(skill_response)}")
            raise InternalException(message="Некорректный формат данных от реестра навыков при создании навыка.")

        return skill_response

    except (BadRequestException, RegistryInteractionException):
        raise
    except ValueError as e:
        logger.error(f"Ошибка сериализации данных навыка '{skill_name}': {e}", exc_info=True)
        raise BadRequestException(
            code="INVALID_SKILL_DATA",
            message=f"Некорректные данные навыка '{skill_name}': {str(e)}"
        ) from e
    except Exception as e:
        logger.error(f"Неожиданная ошибка при добавлении навыка '{skill_name}' в реестр: {e}", exc_info=True)
        raise InternalException(message=f"Внутренняя ошибка сервера при добавлении навыка '{skill_name}'.") from e


async def create_vacancy_skill_link(
        skill_id: UUID,
        vacancy_id: UUID,
        project_id: UUID,
        request: Request
) -> dict:
    """
    Создает связь между вакансией и навыком
    """
    try:
        project_uuid = UUID(str(project_id))
        vacancy_uuid = UUID(str(vacancy_id))
        skill_uuid = UUID(str(skill_id))
    except (ValueError, TypeError) as e:
        raise BadRequestException(
            code="INVALID_UUID",
            message=f"Невалидный UUID для project_id ({project_id}), vacancy_id ({vacancy_id}) или skill_id ({skill_id}): {e}"
        ) from e

    try:
        data_ser = serialize_vacancy_skill_data_to_registry_object(
            project_id=project_uuid,
            vacancy_id=vacancy_uuid,
            skill_id=skill_uuid)

        data = data_ser.model_dump(exclude_none=True)

        link_response = await interact_with_registry(
            method=Method.POST,
            request=request,
            registry_url=settings.RECRUITMENT_REGISTRY_URL,
            registry_name=RegistryName.LINK,
            data=data
        )
        if not isinstance(link_response, dict):
            logger.error(f"Ожидался словарь с данными связи от реестра, но получен {type(link_response)}")
            raise InternalException(message="Некорректный формат данных от реестра связей при создании связи.")

        return link_response

    except (BadRequestException, RegistryInteractionException):
        raise
    except ValueError as e:
        logger.error(f"Ошибка сериализации данных связи навыка {skill_id} с вакансией {vacancy_id}: {e}", exc_info=True)
        raise BadRequestException(
            code="INVALID_LINK_DATA",
            message=f"Некорректные данные связи навыка с вакансией: {str(e)}"
        ) from e
    except Exception as e:
        logger.error(f"Неожиданная ошибка при создании связи навыка {skill_id} с вакансией {vacancy_id}: {e}",
                     exc_info=True)
        raise InternalException(message=f"Внутренняя ошибка сервера при создании связи навыка с вакансией.") from e


async def get_skills_id_from_links(
        object1: UUID,
        request: Request
) -> str:
    """
    Получает строку ID навыков (object2) из реестра связей.
    Если связей нет или ошибка — возвращает пустую строку.
    """
    params = {'object1': object1}

    try:
        links_data = await interact_with_registry(
            method=Method.GET,
            request=request,
            registry_url=settings.RECRUITMENT_REGISTRY_URL,
            registry_name=RegistryName.LINKS,
            params=params,
            raise_not_found=False
        )

        if not links_data:
            return ''

        if not isinstance(links_data, list):
            logger.error(f"Ожидался список связей от реестра, но получен {type(links_data)}")
            return ''

        skills_id = ', '.join([
            item['object2']
            for item in links_data
            if isinstance(item, dict) and 'object2' in item and item['meta']['status'] == 'active'
        ])

        return skills_id

    except RegistryInteractionException as e:
        logger.error(f"Ошибка взаимодействия с реестром связей для object1 {object1}: {e}", exc_info=True)
        return ''
    except Exception as e:
        logger.error(f"Неожиданная ошибка при получении ID навыков из связей для object1 {object1}: {e}", exc_info=True)
        return ''


async def get_skills_info_from_registry_by_ids(
        ids: str,
        request: Request
) -> list:
    """
    Получает названия навыков из реестра
    """
    params = {
        'id': ids
    }
    try:
        skill_info = await interact_with_registry(
            method=Method.GET,
            request=request,
            registry_url=settings.SKILLS_REGISTRY_URL,
            registry_name=RegistryName.SKILLS,
            params=params
        )

        if not isinstance(skill_info, list):
            logger.error(f"Ожидался список навыков от реестра, но получен {type(skill_info)}")
            return []

        skill_names = [
            item.get('data', {}).get('title') for item in skill_info
        ]

        return skill_names

    except RegistryInteractionException as e:
        logger.error(f"Ошибка взаимодействия с реестром навыков при получении по ID: {e}", exc_info=True)
        return []
    except Exception as e:
        logger.error(f"Неожиданная ошибка при получении названий навыков по ID: {e}", exc_info=True)
        return []


async def add_skills_to_vacancy(
        vacancy_data: dict,
        request: Request
) -> dict:
    """
    Добавляет данные навыков к данным вакансии
    """
    try:
        if not isinstance(vacancy_data, dict):
            raise BadRequestException(code="INVALID_VACANCY_DATA", message="Данные вакансии должны быть словарем.")

        skills_ids = await get_skills_id_from_links(
            request=request,
            object1=vacancy_data.get('id')
        )

        if not skills_ids or not skills_ids.strip():
            vacancy_data.setdefault('data', {})['skills'] = []
        else:
            skill_names = await get_skills_info_from_registry_by_ids(
                request=request,
                ids=skills_ids
            )
            vacancy_data.setdefault('data', {})['skills'] = skill_names or []

        return vacancy_data

    except BadRequestException:
        raise
    except Exception as e:
        logger.error(f"Неожиданная ошибка при добавлении навыков к вакансии {vacancy_data.get('id', 'без ID')}: {e}", exc_info=True)
        vacancy_data.setdefault('data', {})['skills'] = []
        return vacancy_data


async def process_skill(
        skill_name: str,
        registry_skills: dict,
        project_id: UUID,
        vacancy_id: UUID,
        request: Request
):
    """
    Обрабатывает навык и создает реестр связи навыка с вакансией
    """
    try:
        if not isinstance(skill_name, str):
            raise BadRequestException(code="INVALID_SKILL_NAME",
                                      message=f"Название навыка должно быть строкой. Получен тип {type(skill_name)}.")
        if not isinstance(registry_skills, dict):
            raise InternalException(message="registry_skills должен быть словарем.")
        if not isinstance(project_id, UUID):
            raise InternalException(message="project_id должен быть UUID.")

        try:
            vacancy_uuid = UUID(str(vacancy_id))
        except (ValueError, TypeError) as e:
            raise InternalException(message=f"Невалидный vacancy_id: {vacancy_id}") from e

        skill_name_lower = skill_name.lower()

        if skill_name_lower in registry_skills:
            skill_id = registry_skills[skill_name_lower]
        else:
            skill_response = await add_vacancy_skill_to_registry(
                skill_name=skill_name,
                project_id=project_id,
                request=request
            )
            skill_id = skill_response.get('id')

            if not skill_id:
                raise InternalException(message=f'Реестр навыков не вернул ID для созданного навыка: {skill_name}')


        vacancy_skill_link = await create_vacancy_skill_link(
            skill_id=skill_id,
            vacancy_id=vacancy_uuid,
            project_id=project_id,
            request=request
        )

        if not vacancy_skill_link or not isinstance(vacancy_skill_link, dict):
            raise InternalException(
                message=f'Реестр связей не вернул данные для созданной связи навыка {skill_name} с вакансией {vacancy_id}')
    except (BadRequestException, RegistryInteractionException):
        raise
    except Exception as e:
        logger.error(f"Неожиданная ошибка при обработке навыка '{skill_name}': {e}", exc_info=True)
        raise InternalException(message=f"Внутренняя ошибка сервера при обработке навыка '{skill_name}'.") from e
