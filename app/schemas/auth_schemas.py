from enum import StrEnum

from pydantic import BaseModel


class DebugMode(StrEnum):
    PROD = "PROD"
    DEV = "DEV"


class AuthConfig(BaseModel):
    mode: DebugMode = None
    methods: dict | None = dict()


class ParamSelection(StrEnum):
    DEBUG_MODE = "DEBUG_MODE"
    PERMISSIONS = "PERMISSIONS"


class MethodState(StrEnum):
    OPEN = "open"
    CLOSED = "closed"
    AUTHORIZED = "authorized"
    BLOCKED = "blocked"
