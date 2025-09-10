from app.config import settings
from fastapi import Request
from uuid import UUID
from app.services.registry_interaction import interact_with_registry
from app.services.serializers.vacancy_serializers import serialize_vacancy_data_to_registry_object
from app.services.utils import Method, RegistryName

from app.exceptions.main_exceptions import BadRequestException, NotFoundException, InternalException
from app.exceptions.sub_exceptions.failed_dependency_exceptions import RegistryInteractionException
import logging

logger = logging.getLogger(__name__)


async def create_vacancy(
        request: Request,
        vacancy_dict: dict,
        project_id: UUID
) -> dict:
    """
    Создает вакансию в реестре
    """
    try:
        if not isinstance(vacancy_dict, dict):
            raise BadRequestException(code="INVALID_VACANCY_DATA", message="Данные вакансии должны быть словарем.")
        if not isinstance(project_id, UUID):
            raise InternalException(message="project_id должен быть UUID.")

        data_ser = serialize_vacancy_data_to_registry_object(
            data=vacancy_dict,
            project_id=project_id
        )
        data = data_ser.model_dump(exclude_none=True)
        try:
            vacancy_response = await interact_with_registry(
                method=Method.POST,
                request=request,
                registry_url=settings.RECRUITMENT_REGISTRY_URL,
                registry_name=RegistryName.RECRUITMENT,
                data=data
            )
            if not isinstance(vacancy_response, dict):
                logger.error(f"Ожидался словарь с данными вакансии от реестра, но получен {type(vacancy_response)}")
                raise InternalException(message="Некорректный формат данных от реестра вакансий при создании вакансии.")

            return vacancy_response
        except RegistryInteractionException:
            raise
        except Exception as e:
            logger.error(f"Ошибка при вызове interact_with_registry для создания вакансии: {e}", exc_info=True)
            raise RegistryInteractionException(registry_error=f"Ошибка при создании вакансии: {str(e)}") from e

    except BadRequestException:
        raise
    except ValueError as e:
        logger.error(f"Ошибка сериализации данных вакансии: {e}", exc_info=True)
        raise BadRequestException(
            code="INVALID_VACANCY_DATA",
            message=f"Некорректные данные вакансии: {str(e)}"
        ) from e
    except RegistryInteractionException:
        raise
    except Exception as e:
        logger.error(f"Неожиданная ошибка при создании вакансии: {e}", exc_info=True)
        raise InternalException(message="Внутренняя ошибка сервера при создании вакансии.") from e


async def update_vacancy(
        request: Request,
        vacancy_update_dict: dict,
        vacancy_id: UUID
) -> dict:
    """
    Обновляет вакансию в реестре
    """
    if not vacancy_update_dict:
        raise BadRequestException(
            code="EMPTY_UPDATE_DATA",
            message="Нет данных для обновления"
        )

    if not isinstance(vacancy_update_dict, dict):
        raise BadRequestException(code="INVALID_UPDATE_DATA", message="Данные для обновления должны быть словарем.")

    try:
        vacancy_uuid = UUID(str(vacancy_id))
    except (ValueError, TypeError) as e:
        raise InternalException(message=f"Невалидный vacancy_id: {vacancy_id}") from e

    try:
        vacancy_update_response = await interact_with_registry(
            method=Method.PATCH,
            request=request,
            registry_url=settings.RECRUITMENT_REGISTRY_URL,
            registry_name=RegistryName.RECRUITMENT,
            _id=vacancy_uuid,
            data=vacancy_update_dict
        )

        if not isinstance(vacancy_update_response, dict):
            logger.error(f"Ожидался словарь с данными вакансии от реестра, но получен {type(vacancy_update_response)}")
            raise InternalException(message="Некорректный формат данных от реестра вакансий при обновлении вакансии.")

        return vacancy_update_response

    except (NotFoundException, BadRequestException, RegistryInteractionException):
        raise
    except Exception as e:
        logger.error(f"Неожиданная ошибка при обновлении вакансии {vacancy_id}: {e}", exc_info=True)
        raise InternalException(message=f"Внутренняя ошибка сервера при обновлении вакансии {vacancy_id}.") from e


async def get_links_ids(
        object1: UUID,
        request: Request
) -> str:
    """
    Получает строку ID реестров связей.
    Если связей нет или ошибка — возвращает пустую строку.
    """
    if not isinstance(object1, UUID):
        logger.error("object1 должен быть UUID.")
        return ''

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

        links_ids = ','.join([
            item['id']
            for item in links_data
            if isinstance(item, dict) and 'id' in item and item['meta']['status'] == 'active'
        ])
        return links_ids
    except RegistryInteractionException as e:
        logger.error(f"Ошибка взаимодействия с реестром связей для object1 {object1}: {e}", exc_info=True)
        return ''
    except Exception as e:
        logger.error(f"Неожиданная ошибка при получении ID связей для object1 {object1}: {e}", exc_info=True)
        return ''


async def add_skills_to_vacancies(
        vacancies_data: list[dict],
        request: Request
) -> list[dict]:
    """
    Добавление данных навыков к данным вакансий.
    Выполняет пакетные запросы к реестрам для минимизации сетевых вызовов.
    """
    try:
        if not vacancies_data:
            return []

        vacancy_ids = [vacancy.get('id') for vacancy in vacancies_data if vacancy.get('id')]
        if not vacancy_ids:
            for vacancy in vacancies_data:
                vacancy.setdefault('data', {})['skills'] = []
            return vacancies_data

        vacancy_ids_str = ','.join(str(v_id) for v_id in vacancy_ids)
        links_params = {'object1': vacancy_ids_str}

        try:
            all_links_data = await interact_with_registry(
                method=Method.GET,
                request=request,
                registry_url=settings.RECRUITMENT_REGISTRY_URL,
                registry_name=RegistryName.LINKS,
                params=links_params,
                raise_not_found=False
            )
        except RegistryInteractionException as e:
            logger.warning(f"Ошибка при получении связей для вакансий: {e}. Продолжаем без навыков.")
            for vacancy in vacancies_data:
                vacancy.setdefault('data', {})['skills'] = []
            return vacancies_data

        except Exception as e:
            logger.error(f"Неожиданная ошибка при получении связей для вакансий: {e}", exc_info=True)
            for vacancy in vacancies_data:
                vacancy.setdefault('data', {})['skills'] = []
            return vacancies_data

        vacancy_to_skills = {v_id: [] for v_id in vacancy_ids}
        if isinstance(all_links_data, list):
            for link_item in all_links_data:
                if isinstance(link_item, dict):
                    meta = link_item.get('meta', {})
                    if isinstance(meta, dict) and meta.get('status') == 'active':
                        object1 = link_item.get('object1')
                        object2 = link_item.get('object2')
                        if object1 and object2 and object1 in vacancy_ids:
                            vacancy_to_skills[object1].append(str(object2))

        all_skill_ids = set()
        for skill_ids in vacancy_to_skills.values():
            all_skill_ids.update(skill_ids)

        if not all_skill_ids:
            for vacancy in vacancies_data:
                vacancy_id = vacancy.get('id')
                if vacancy_id:
                    vacancy.setdefault('data', {})['skills'] = []
            return vacancies_data

        skill_ids_str = ','.join(all_skill_ids)
        skills_params = {'id': skill_ids_str}

        try:
            all_skills_info = await interact_with_registry(
                method=Method.GET,
                request=request,
                registry_url=settings.SKILLS_REGISTRY_URL,
                registry_name=RegistryName.SKILLS,
                params=skills_params
            )
        except RegistryInteractionException as e:
            logger.warning(f"Ошибка при получении информации о навыках: {e}. Продолжаем без названий навыков.")
            for vacancy in vacancies_data:
                vacancy_id = vacancy.get('id')
                if vacancy_id and vacancy_id in vacancy_to_skills:
                    vacancy.setdefault('data', {})['skills'] = vacancy_to_skills[vacancy_id]
            return vacancies_data

        except Exception as e:
            logger.error(f"Неожиданная ошибка при получении информации о навыках: {e}", exc_info=True)
            for vacancy in vacancies_data:
                vacancy_id = vacancy.get('id')
                if vacancy_id and vacancy_id in vacancy_to_skills:
                    vacancy.setdefault('data', {})['skills'] = vacancy_to_skills[vacancy_id]
            return vacancies_data

        skill_id_to_name = {}
        if isinstance(all_skills_info, list):
            for skill_item in all_skills_info:
                if isinstance(skill_item, dict):
                    skill_id = skill_item.get('id')
                    skill_data = skill_item.get('data', {})
                    if isinstance(skill_data, dict):
                        skill_name = skill_data.get('title')
                        if skill_id and skill_name:
                            skill_id_to_name[str(skill_id)] = skill_name

        for vacancy in vacancies_data:
            vacancy_id = vacancy.get('id')
            if vacancy_id and vacancy_id in vacancy_to_skills:
                skill_ids_for_vacancy = vacancy_to_skills[vacancy_id]
                skill_names = []
                for skill_id in skill_ids_for_vacancy:
                    skill_name = skill_id_to_name.get(skill_id, skill_id)
                    skill_names.append(skill_name)
                vacancy.setdefault('data', {})['skills'] = skill_names
            else:
                vacancy.setdefault('data', {})['skills'] = []

        return vacancies_data

    except Exception as e:
        logger.error(f"Неожиданная ошибка в add_skills_to_vacancies_batch: {e}", exc_info=True)
        for vacancy in vacancies_data:
            vacancy.setdefault('data', {})['skills'] = []
        return vacancies_data