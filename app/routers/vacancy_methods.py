import asyncio
from uuid import UUID
from fastapi import APIRouter, Request, Header
from app.config import settings
from app.schemas.response_schemas import SuccessfulResponse, ResponseDetail
from app.schemas.vacancy_schemas import VacancyInputData, VacancyUpdateData
from app.services.registry_interaction import interact_with_registry
from app.services.skill_utils import get_skills_from_vacancy, get_all_skills_from_registry, \
    get_skills_id_from_links, \
    get_skills_info_from_registry_by_ids, process_skill
from app.services.utils import HeaderAlias, Method, RegistryName
from app.services.vacancy_utils import create_vacancy, update_vacancy, get_links_ids
from app.exceptions.main_exceptions import BadRequestException, NotFoundException, InternalException
from app.exceptions.sub_exceptions.failed_dependency_exceptions import RegistryInteractionException
import logging


logger = logging.getLogger(__name__)

router = APIRouter(prefix='/vacancy', tags=['Вакансия'])


@router.get(
    '/{vacancy_id}',
    response_model=SuccessfulResponse,
    response_model_exclude_unset=True,
    summary='Получить вакансию по её ID'
)
async def get_vacancy_by_id(
        request: Request,
        vacancy_id: UUID,
        project_id: UUID = Header(..., alias=HeaderAlias.PROJECT_ID)
) -> SuccessfulResponse:
    """
    Получает данные вакансии по её ID.
    """
    params = {
        'project_id': project_id
    }
    try:
        vacancy_data = await interact_with_registry(
            method=Method.GET,
            request=request,
            registry_url=settings.RECRUITMENT_REGISTRY_URL,
            registry_name=RegistryName.RECRUITMENT,
            _id=vacancy_id,
            params=params
        )

        if not isinstance(vacancy_data, dict):
            logger.error(f"Ожидался словарь с данными вакансии, но получен {type(vacancy_data)}")
            raise InternalException(message="Некорректный формат данных от реестра вакансий.")

        skills_ids = await get_skills_id_from_links(
            request=request,
            object1=vacancy_id
        )

        if not skills_ids or not skills_ids.strip():
            vacancy_data.setdefault('data', {})['skills'] = []
        else:
            skill_names = await get_skills_info_from_registry_by_ids(
                request=request,
                ids=skills_ids
            )
            vacancy_data['data']['skills'] = skill_names or []

        return SuccessfulResponse(
            detail=ResponseDetail(
                code='OK',
                message='Данные вакансии успешно получены'
            ),
            data=[vacancy_data]
        )

    except NotFoundException:
        raise
    except RegistryInteractionException as e:
        logger.error(f"Ошибка взаимодействия с реестром при получении вакансии {vacancy_id}: {e}", exc_info=True)
        raise
    except Exception as e:
        logger.error(f"Неожиданная ошибка при получении вакансии {vacancy_id}: {e}", exc_info=True)
        raise InternalException(message="Внутренняя ошибка сервера при получении вакансии.") from e


@router.patch(
    '/{vacancy_id}',
    response_model=SuccessfulResponse,
    response_model_exclude_unset=True,
    summary='Обновить вакансию по её ID'
)
async def update_vacancy_by_id(
        request: Request,
        vacancy_id: UUID,
        vacancy_update_data: VacancyUpdateData,
        project_id: UUID = Header(..., alias=HeaderAlias.PROJECT_ID)
) -> SuccessfulResponse:
    """
    Обновляет основные данные вакансии и при необходимости обновляет связанные навыки.
    """
    try:
        vacancy_update_dict = vacancy_update_data.model_dump(exclude_unset=True)

        if 'skills' in vacancy_update_dict.get('data'):
            vacancy_update_skills = get_skills_from_vacancy(vacancy_update_dict.get('data', {}))

            old_links_ids = await get_links_ids(
                request=request,
                object1=vacancy_id
            )

            if old_links_ids:
                await interact_with_registry(
                    method=Method.DELETE,
                    request=request,
                    registry_url=settings.RECRUITMENT_REGISTRY_URL,
                    registry_name=RegistryName.LINKS,
                    params={'id': old_links_ids}
                )

            registry_skills = await get_all_skills_from_registry(
                project_id=project_id,
                request=request
            )

            tasks = [
                process_skill(
                    skill_name=skill_name,
                    registry_skills=registry_skills,
                    project_id=project_id,
                    vacancy_id=vacancy_id,
                    request=request
                )
                for skill_name in vacancy_update_skills
            ]

            results = await asyncio.gather(*tasks, return_exceptions=True)
            errors = []
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    skill_name = vacancy_update_skills[i]
                    error_msg = f'Ошибка при обработке навыка "{skill_name}" при обновлении вакансии: {str(result)}'
                    logger.error(error_msg, exc_info=True)
                    errors.append(error_msg)

            if errors:
                logger.warning(f"Ошибки при обработке навыков: {errors}")

        update_vacancy_data = await update_vacancy(
            request=request,
            vacancy_update_dict=vacancy_update_dict,
            vacancy_id=vacancy_id
        )

        return SuccessfulResponse(
            detail=ResponseDetail(
                code='OK',
                message='Вакансия успешно обновлена'
            ),
            data=[update_vacancy_data]
        )

    except (NotFoundException, BadRequestException):
        raise
    except RegistryInteractionException as e:
        logger.error(f"Ошибка взаимодействия с реестром при обновлении вакансии {vacancy_id}: {e}", exc_info=True)
        raise
    except Exception as e:
        logger.error(f"Неожиданная ошибка при обновлении вакансии {vacancy_id}: {e}", exc_info=True)
        raise InternalException(message="Внутренняя ошибка сервера при обновлении вакансии.") from e


@router.post(
    '/',
    response_model=SuccessfulResponse,
    response_model_exclude_unset=True,
    summary='Создать новую вакансию'
)
async def create_vacancy_and_link(
        request: Request,
        vacancy_data: VacancyInputData,
        project_id: UUID = Header(..., alias=HeaderAlias.PROJECT_ID)
) -> SuccessfulResponse:
    """
    Создает новую вакансию.
    """
    try:
        vacancy_dict = vacancy_data.model_dump()

        vacancy_skills = get_skills_from_vacancy(vacancy_dict)

        vacancy = await create_vacancy(
            request=request,
            vacancy_dict=vacancy_dict,
            project_id=project_id
        )

        vacancy_id = vacancy.get('id')
        if not vacancy_id:
            raise InternalException(message='Не удалось получить ID созданной вакансии')

        try:
            vacancy_uuid = UUID(str(vacancy_id))
        except (ValueError, TypeError) as e:
            raise InternalException(message=f'Реестр вернул невалидный ID для созданной вакансии: {vacancy_id}') from e

        registry_skills = await get_all_skills_from_registry(
            project_id=project_id,
            request=request
        )

        if vacancy_skills:
            tasks = [
                process_skill(
                    skill_name=skill_name,
                    registry_skills=registry_skills,
                    project_id=project_id,
                    vacancy_id=vacancy_uuid,
                    request=request
                )
                for skill_name in vacancy_skills
            ]

            results = await asyncio.gather(*tasks, return_exceptions=True)
            errors = []
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    skill_name = vacancy_skills[i]
                    error_msg = f'Ошибка при обработке навыка "{skill_name}" при создании вакансии: {str(result)}'
                    logger.error(error_msg, exc_info=True)
                    errors.append(error_msg)

            if errors:
                logger.warning(f"Ошибки при обработке навыков: {errors}")

        return SuccessfulResponse(
            detail=ResponseDetail(
                code='CREATED',
                message='Вакансия успешно создана'
            ),
            data=[vacancy]
        )

    except BadRequestException:
        raise
    except RegistryInteractionException as e:
        logger.error(f"Ошибка взаимодействия с реестром при создании вакансии: {e}", exc_info=True)
        raise
    except Exception as e:
        logger.error(f"Неожиданная ошибка при создании вакансии: {e}", exc_info=True)
        raise InternalException(message="Внутренняя ошибка сервера при создании вакансии.") from e


@router.delete(
    '/{vacancy_id}',
    response_model=SuccessfulResponse,
    response_model_exclude_unset=True,
    summary='Удалить вакансию по её ID'
)
async def delete_vacancy(
        request: Request,
        vacancy_id: UUID,
) -> SuccessfulResponse:
    """
    Удаляет вакансию по её ID.
    """
    try:
        response_data = await interact_with_registry(
            method=Method.DELETE,
            request=request,
            registry_url=settings.RECRUITMENT_REGISTRY_URL,
            registry_name=RegistryName.RECRUITMENT,
            _id=vacancy_id
        )

        if not response_data:
            raise NotFoundException('Вакансия не найдена')

        return SuccessfulResponse(
            detail=ResponseDetail(
                code='OK',
                message='Вакансия успешно удалена'
            ),
            data=[]
        )

    except NotFoundException:
        raise
    except RegistryInteractionException as e:
        logger.error(f"Ошибка взаимодействия с реестром при удалении вакансии {vacancy_id}: {e}", exc_info=True)
        raise
    except Exception as e:
        logger.error(f"Неожиданная ошибка при удалении вакансии {vacancy_id}: {e}", exc_info=True)
        raise InternalException(message="Внутренняя ошибка сервера при удалении вакансии.") from e

