import asyncio
from uuid import UUID
from fastapi import APIRouter, Request, Header

from app.config import settings
from app.exceptions.sub_exceptions.failed_dependency_exceptions import RegistryInteractionException
from app.schemas.response_schemas import SuccessfulResponse, ResponseDetail
from app.schemas.vacancy_schemas import VacancyInputData

from app.services.registry_interaction import interact_with_registry
from app.services.skill_utils import add_skills_to_vacancy, get_all_skills_from_registry, get_skills_from_vacancy, \
    process_skill
from app.services.utils import HeaderAlias, Method, RegistryName
from app.exceptions.main_exceptions import BadRequestException, NotFoundException, ServiceException, InternalException
from app.services.vacancy_utils import create_vacancy
import logging


logger = logging.getLogger(__name__)

router = APIRouter(prefix='/vacancies', tags=['Вакансии'])


@router.get(
    '/',
    response_model=SuccessfulResponse,
    response_model_exclude_unset=True,
    summary='Получить все вакансии проекта'
)
async def get_vacancies(
        request: Request,
        project_id: UUID = Header(..., alias=HeaderAlias.PROJECT_ID)
) -> SuccessfulResponse:
    """
    Получает все вакансии.
    """
    params = {'project_id': project_id}
    try:
        vacancies_data = await interact_with_registry(
            method=Method.GET,
            request=request,
            registry_url=settings.RECRUITMENT_REGISTRY_URL,
            registry_name=RegistryName.RECRUITMENTS,
            params=params
        )
        if not isinstance(vacancies_data, list):
            logger.error(f"Ожидался список вакансий, но получен {type(vacancies_data)}")
            raise InternalException(message="Некорректный формат данных от реестра вакансий.")

        tasks = [add_skills_to_vacancy(vacancy, request) for vacancy in vacancies_data]
        full_vacancies_data = await asyncio.gather(*tasks)

        return SuccessfulResponse(
            detail=ResponseDetail(
                code='OK',
                message='Данные вакансий успешно получены'
            ),
            data=full_vacancies_data
        )

    except NotFoundException:
        raise
    except RegistryInteractionException as e:
        logger.error(f"Ошибка взаимодействия с реестром при получении вакансий: {e}", exc_info=True)
        raise
    except ServiceException as e:
        logger.error(f"Сервисная ошибка при получении вакансий: {e}", exc_info=True)
        raise
    except Exception as e:
        logger.error(f"Неожиданная ошибка при получении вакансий: {e}", exc_info=True)
        raise InternalException(message="Внутренняя ошибка сервера при получении вакансий.") from e


@router.post(
    '/',
    response_model=SuccessfulResponse,
    response_model_exclude_unset=True,
    summary='Создать вакансии'
)
async def create_vacancies(
        request: Request,
        vacancies_data: list[VacancyInputData],
        project_id: UUID = Header(..., alias=HeaderAlias.PROJECT_ID)
) -> SuccessfulResponse:
    """
    Создает несколько новых вакансий.
    """
    try:
        created_vacancies = []
        errors = []

        registry_skills = await get_all_skills_from_registry(
            project_id=project_id,
            request=request
        )

        for vacancy_data in vacancies_data:
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
                    raise InternalException(
                        message=f'Реестр вернул невалидный ID для созданной вакансии: {vacancy_id}') from e

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
                    for i, result in enumerate(results):
                        if isinstance(result, Exception):
                            skill_name = vacancy_skills[i]
                            error_msg = f'Ошибка при обработке навыка "{skill_name}": {str(result)}'
                            logger.error(error_msg, exc_info=True)
                            errors.append(error_msg)

                created_vacancies.append(vacancy)

            except BadRequestException as e:
                error_msg = f'Ошибка при создании вакансии {vacancy_dict.get("title", "без названия")}: {str(e)}'
                logger.warning(error_msg)
                errors.append(error_msg)
                continue
            except RegistryInteractionException as e:
                error_msg = f'Ошибка взаимодействия с реестром при создании вакансии {vacancy_dict.get("title", "без названия")}: {str(e)}'
                logger.error(error_msg, exc_info=True)
                errors.append(error_msg)
                continue
            except Exception as e:
                error_msg = f'Неожиданная ошибка при создании вакансии {vacancy_dict.get("title", "без названия")}: {str(e)}'
                logger.error(error_msg, exc_info=True)
                errors.append(error_msg)
                continue

        if not created_vacancies:
            raise BadRequestException(message='Не удалось создать ни одной вакансии. Подробности в логах.')

        return SuccessfulResponse(
            detail=ResponseDetail(
                code='CREATED',
                message=f'Успешно создано {len(created_vacancies)} из {len(vacancies_data)} вакансий'
            ),
            data=created_vacancies
        )

    except BadRequestException:
        raise
    except RegistryInteractionException as e:
        logger.error(f"Ошибка взаимодействия с реестром при создании вакансий: {e}", exc_info=True)
        raise
    except Exception as e:
        logger.error(f"Неожиданная ошибка при создании вакансий: {e}", exc_info=True)
        raise InternalException(message="Внутренняя ошибка сервера при создании вакансий.") from e