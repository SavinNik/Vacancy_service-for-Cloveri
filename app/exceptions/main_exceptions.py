from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder

from ..schemas.response_schemas import ResponseDetail


class ServiceException(HTTPException):
    def __init__(self, status_code: int = 500, code: str = None, message: str = None):
        self.status_code = status_code
        self._detail = ResponseDetail(code=code, message=message)
        super().__init__(status_code=self.status_code, detail=jsonable_encoder(self._detail))


class InternalException(ServiceException):
    def __init__(self, code="INTERNAL_SERVER_ERROR", message="Внутренняя ошибка компонентов сервера."):
        super().__init__(code=code, message=message)


class BadRequestException(ServiceException):
    def __init__(self, code="BAD_REQUEST", message="Ошибка форматного контроля."):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, code=code, message=message)


class ForbiddenException(ServiceException):
    def __init__(self, code="FORBIDDEN", message="Доступ запрещен."):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, code=code, message=message)


class NotFoundException(ServiceException):
    def __init__(self, code="NOT_FOUND", message="Объект не найден."):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, code=code, message=message)


class FailedDependencyException(ServiceException):
    def __init__(self, code="FAILED_DEPENDENCY", message="Ошибка при взаимодействии с зависимым компонентом."):
        super().__init__(status_code=status.HTTP_424_FAILED_DEPENDENCY, code=code, message=message)
