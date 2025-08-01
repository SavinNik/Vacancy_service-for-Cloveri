from ..main_exceptions import InternalException


class InvalidMethodException(InternalException):
    def __init__(self):
        super().__init__(message="Метод не поддерживается.")

class DebugModeNotFoundException(Exception):
    def __init__(self, message="Укажите DEBUG_MODE в AUTH."):
        super().__init__(message)
