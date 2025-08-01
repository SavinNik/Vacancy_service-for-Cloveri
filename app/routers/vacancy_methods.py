from uuid import UUID
from fastapi import APIRouter, Request, Header
from fastapi.encoders import jsonable_encoder

from app.config import settings
from app.schemas.response_schemas import SuccessfulResponse, ResponseDetail
from app.schemas.vacancy_schemas import VacancyData, VacancyUpdateData
from app.services.registry_interaction import interact_with_registry
from app.services.serializers.vacancy_serializers import serialize_vacancy_data_to_registry_object
from app.services.utils import HeaderAlias, Method, RegistryName
from app.exceptions.main_exceptions import BadRequestException, NotFoundException

router = APIRouter(prefix='/vacancy', tags=['Вакансия'])


@router.get(
    "/{vacancy_id}",
    response_model=SuccessfulResponse,
    response_model_exclude_unset=True,
    summary="Получить вакансию по её ID"
)
async def get_vacancy_by_id(
        request: Request,
        vacancy_id: UUID,
        project_id: UUID = Header(..., alias=HeaderAlias.PROJECT_ID)
) -> SuccessfulResponse:
    """
    Получает данные вакансии по её ID.
    """
    try:
        response_data = await interact_with_registry(
            method=Method.GET,
            request=request,
            registry_url=settings.RECRUITMENT_REGISTRY_URL,
            registry_name=RegistryName.RECRUITMENT,
            _id=vacancy_id
        )

        if not response_data:
            raise NotFoundException("Вакансия не найдена")

        return SuccessfulResponse(
            detail=ResponseDetail(
                code='OK',
                message='Данные вакансии успешно получены'
            ),
            data=[response_data]
        )

    except Exception as e:
        raise BadRequestException(str(e))


@router.patch(
    "/{vacancy_id}",
    response_model=SuccessfulResponse,
    response_model_exclude_unset=True,
    summary="Обновить вакансию по её ID"
)
async def update_vacancy_by_id(
        request: Request,
        vacancy_id: UUID,
        vacancy_data: VacancyUpdateData,
        project_id: UUID = Header(..., alias=HeaderAlias.PROJECT_ID)
) -> SuccessfulResponse:
    """
    Частично обновляет данные вакансии.
    Обновляются только переданные поля.
    """
    try:
        response_data = await interact_with_registry(
            method=Method.PATCH,
            request=request,
            registry_url=settings.RECRUITMENT_REGISTRY_URL,
            registry_name=RegistryName.RECRUITMENT,
            _id=vacancy_id,
            data=vacancy_data.model_dump(exclude_unset=True)
        )

        if not response_data:
            raise NotFoundException("Вакансия не найдена")

        return SuccessfulResponse(
            detail=ResponseDetail(
                code='OK',
                message='Вакансия успешно обновлена'
            ),
            data=[response_data]
        )

    except Exception as e:
        raise BadRequestException(str(e))


@router.post(
    "/",
    response_model=SuccessfulResponse,
    response_model_exclude_unset=True,
    summary="Создать новую вакансию"
)
async def create_vacancy(
        request: Request,
        vacancy_data: VacancyData,
        project_id: UUID = Header(..., alias=HeaderAlias.PROJECT_ID)
) -> SuccessfulResponse:
    """
    Создает новую вакансию.
    """
    try:
        data = serialize_vacancy_data_to_registry_object(data=vacancy_data)
        response_data = await interact_with_registry(
            method=Method.POST,
            request=request,
            registry_url=settings.RECRUITMENT_REGISTRY_URL,
            registry_name=RegistryName.RECRUITMENT,
            data=data
        )

        if not response_data:
            raise BadRequestException("Не удалось создать вакансию")

        return SuccessfulResponse(
            detail=ResponseDetail(
                code='CREATED',
                message='Вакансия успешно создана'
            ),
            data=[response_data]
        )

    except Exception as e:
        raise BadRequestException(str(e))


@router.put(
    "/{vacancy_id}",
    response_model=SuccessfulResponse,
    response_model_exclude_unset=True,
    summary="Заменить вакансию по её ID"
)
async def replace_vacancy_by_id(
        request: Request,
        vacancy_id: UUID,
        vacancy_data: VacancyData,
        project_id: UUID = Header(..., alias=HeaderAlias.PROJECT_ID)
) -> SuccessfulResponse:
    """
    Полностью заменяет данные вакансии.
    Требует отправки всех обязательных полей.
    """
    try:
        data = serialize_vacancy_data_to_registry_object(data=vacancy_data)

        response_data = await interact_with_registry(
            method=Method.PUT,
            request=request,
            registry_url=settings.RECRUITMENT_REGISTRY_URL,
            registry_name=RegistryName.RECRUITMENT,
            _id=vacancy_id,
            data=data
        )

        if not response_data:
            raise NotFoundException("Вакансия не найдена")

        return SuccessfulResponse(
            detail=ResponseDetail(
                code='OK',
                message='Вакансия успешно заменена'
            ),
            data=[response_data] if response_data else []
        )

    except Exception as e:
        raise BadRequestException(str(e))


@router.delete(
    "/{vacancy_id}",
    response_model=SuccessfulResponse,
    response_model_exclude_unset=True,
    summary="Удалить вакансию по её ID"
)
async def delete_vacancy(
        request: Request,
        vacancy_id: UUID,
        project_id: UUID = Header(..., alias=HeaderAlias.PROJECT_ID)
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
            raise NotFoundException("Вакансия не найдена")

        return SuccessfulResponse(
            detail=ResponseDetail(
                code='OK',
                message='Вакансия успешно удалена'
            ),
            data=[]
        )

    except Exception as e:
        raise BadRequestException(str(e))