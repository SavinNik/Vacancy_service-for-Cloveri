from app.exceptions.main_exceptions import FailedDependencyException


class RegistryInteractionException(FailedDependencyException):
    def __init__(self, registry_error: str = None):
        super().__init__(code="REGISTRY_ERROR", message="Сервис реестров вернул ошибку: " + registry_error)


class IncorrectFormatInRegistryException(FailedDependencyException):
    def __init__(self):
        super().__init__(code="REGISTRY_ERROR", message="Ошибка при взаимодействии с реестром.")


class IncorrectFormatInServiceException(FailedDependencyException):
    def __init__(self):
        super().__init__(code="SERVICE_ERROR", message="Ошибка при взаимодействии с внешним сервисом.")


class ServiceInteractionException(FailedDependencyException):
    def __init__(self, service_error: str = None):
        super().__init__(code="SERVICE_ERROR", message="Сервис вернул ошибку: " + service_error)
