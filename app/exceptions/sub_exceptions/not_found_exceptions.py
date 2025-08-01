from ..main_exceptions import NotFoundException


class ProfilesNotFoundException(NotFoundException):
    def __init__(self):
        super().__init__(message="Профилей не найдено.")


class RegistryObjectDeactivatedException(NotFoundException):
    def __init__(self):
        super().__init__(message="Данный объект был удален.")
