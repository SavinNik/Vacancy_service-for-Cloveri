from uuid import UUID
from fastapi import APIRouter, Request, Header


from app.config import settings
from app.schemas.response_schemas import SuccessfulResponse, ResponseDetail

from app.services.registry_interaction import interact_with_registry
from app.services.utils import HeaderAlias, Method, RegistryName
from app.exceptions.main_exceptions import BadRequestException, NotFoundException


router = APIRouter(prefix='/vacancies', tags=['Вакансии'])


@router.get(
    "/",
    response_model=SuccessfulResponse,
    response_model_exclude_unset=True,
    summary="Получить все вакансии"
)
async def get_vacancies(
        request: Request,
        project_id: UUID = Header(..., alias=HeaderAlias.PROJECT_ID)
) -> SuccessfulResponse:
    """
    Получает все вакансии.
    """
    try:
        response_data = await interact_with_registry(
            method=Method.GET,
            request=request,
            registry_url=settings.RECRUITMENT_REGISTRY_URL,
            registry_name=RegistryName.RECRUITMENTS,
        )

        if not response_data:
            raise NotFoundException("Вакансии не найдены")

        return SuccessfulResponse(
            detail=ResponseDetail(
                code='OK',
                message='Данные вакансий успешно получены'
            ),
            data=[response_data]
        )

    except Exception as e:
        raise BadRequestException(str(e))