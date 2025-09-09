from enum import StrEnum, IntEnum

from app.config import settings


class Method(IntEnum):
    GET = 1
    POST = 2
    PUT = 3
    PATCH = 4
    DELETE = 5


class HeaderAlias(StrEnum):
    PROJECT_ID = "Project-ID"
    # AUTHORIZATION = "Authorization"


class RegistryName(StrEnum):
    RECRUITMENT = "recruitment"
    RECRUITMENTS = "recruitments"

    SKILL = "skill"
    SKILLS = "skills"

    LINK = "link"
    LINKS = "links"


# class Handle(StrEnum):
#     RECRUITMENT = "recruitment"
#     RECRUITMENT_ID = "recruitment/{id}"
#
#
#     def resolve(self, **kwargs):
#         return self.value.format(**kwargs)


def get_public_key() -> bytes:
    return settings.ACCESS_TOKEN_PUBLIC_KEY.replace("\\n", "\n").encode()
