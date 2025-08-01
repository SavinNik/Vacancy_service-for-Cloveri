from json import JSONDecodeError
from uuid import UUID

from fastapi import Request, status

from app.exceptions.main_exceptions import ServiceException
from app.exceptions.sub_exceptions.failed_dependency_exceptions import IncorrectFormatInServiceException, \
    ServiceInteractionException
from app.exceptions.sub_exceptions.internal_exceptions import InvalidMethodException
from app.exceptions.sub_exceptions.not_found_exceptions import ProfilesNotFoundException
from app.services.utils import Method, HeaderAlias, Handle
from app.config import settings


async def interact_with_api(
        request: Request,
        method: Method,
        api_url: str,
        handle: str,
        headers: dict | None = None,
        params: dict | None = None
):
    url = api_url + handle

    if headers:
        headers[HeaderAlias.AUTHORIZATION] = request.headers.get(HeaderAlias.AUTHORIZATION)
    else:
        headers = {HeaderAlias.AUTHORIZATION: request.headers.get(HeaderAlias.AUTHORIZATION)}

    client = request.app.requests_client

    try:
        match method:
            case Method.GET:
                response = await client.get(url, params=params, headers=headers)
            case _:
                raise InvalidMethodException
    except InvalidMethodException:
        raise InvalidMethodException
    except Exception as e:
        print(f"Ошибка в методе interact_with_api.\nСервис {api_url} вернул ошибку.")
        error = f"{e.get("detail") if isinstance(e, dict) and "detail" in e else str(e)}"
        raise ServiceInteractionException(service_error=error)

    try:
        response_info = response.json()
    except JSONDecodeError as e:
        print(e)
        raise IncorrectFormatInServiceException

    if response.status_code not in (status.HTTP_200_OK, status.HTTP_201_CREATED):
        if response_info and response_info.get('detail'):
            if type(response_info.get('detail')) is dict and response_info.get('detail').get('code') \
                and response_info.get('detail').get('message'):
                code = response_info.get('detail').get('code')
                message = response_info.get('detail').get('message')
                raise ServiceException(status_code=response.status_code, code=code, message=message)
        print(f"Ошибка в методе interact_with_api.\nСервис {api_url} вернул ошибку.")
        raise ServiceInteractionException(service_error=f"{response, response_info}")

    return response_info


async def get_profile_entries_by_project_id(
        request: Request,
        project_id: UUID,
        limit: int,
        offset: int | None
) -> list:
    headers = {HeaderAlias.PROJECT_ID: str(project_id)}

    params = {
        "project_id": project_id,
        "limit": min(limit, 200),
        "offset": offset
    }

    try:
        profile_data = await interact_with_api(
            request=request,
            method=Method.GET,
            api_url=settings.USER_PROFILES_API_URL,
            handle=Handle.PROFILES.resolve(),
            headers=headers,
            params=params
        )
        return profile_data.get('data')
    except ServiceException as e:
        if e.status_code == status.HTTP_404_NOT_FOUND:
            raise ProfilesNotFoundException
        raise e
