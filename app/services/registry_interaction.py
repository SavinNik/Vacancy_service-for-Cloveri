from uuid import UUID

from fastapi import Request, status
from fastapi.encoders import jsonable_encoder

from app.exceptions.main_exceptions import NotFoundException
from app.exceptions.sub_exceptions.bad_request_exceptions import EntityExistsException
from app.exceptions.sub_exceptions.failed_dependency_exceptions import RegistryInteractionException, \
    IncorrectFormatInRegistryException
from app.exceptions.sub_exceptions.not_found_exceptions import RegistryObjectDeactivatedException
from app.schemas.base_schemas import RegistryObject, LinkObject
from app.services.utils import Method


async def interact_with_registry(
    method: Method,
    request: Request,
    registry_url: str,
    registry_name: str,
    _id: UUID = None,
    params: dict = None,
    data: RegistryObject | LinkObject | list | dict = None,
    active_records: bool = True,
    raise_not_found: bool = True
) -> dict | list[dict]:
    if not _id:
        registry_url = f"{registry_url}/{registry_name}/"
    else:
        registry_url = f"{registry_url}/{registry_name}/{_id}/"
    data = jsonable_encoder(data)
    request_client = request.app.requests_client

    try:
        match method:
            case (Method.GET):
                response = await request_client.get(registry_url, params=params)
            case (Method.POST):
                response = await request_client.post(registry_url, json=data)
            case (Method.PUT):
                response = await request_client.put(registry_url, json=data)
            case (Method.PATCH):
                response = await request_client.patch(registry_url, json=data)
            case (Method.DELETE):
                response = await request_client.delete(registry_url)
    except Exception as e:
        print(f"Ошибка в методе interact_with_registry.\n"
              f"Тип исключения: {type(e).__name__}\nСообщение: {str(e)}\n"
              f"Объект: {data}")
        raise RegistryInteractionException(registry_error=str(e))

    try:
        response_data = response.json()
    except Exception as e:
        print(f"Ошибка в методе interact_with_registry.\n"
              f"Тип исключения: {type(e).__name__}\nСообщение: {str(e)}\n"
              f"Объект: {data}")
        raise IncorrectFormatInRegistryException

    if raise_not_found and (response.status_code == status.HTTP_404_NOT_FOUND or not response_data):
        raise NotFoundException

    if response.status_code == status.HTTP_400_BAD_REQUEST and 'exists' in str(response.json()):
        raise EntityExistsException

    if response.status_code not in (status.HTTP_200_OK, status.HTTP_201_CREATED):
        raise RegistryInteractionException(registry_error=f"{response.json()}")

    if active_records and "meta" in response.json() and response.json()["meta"]["status"] == "inactive":
        raise RegistryObjectDeactivatedException

    return response_data
