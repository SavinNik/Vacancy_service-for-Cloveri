# from functools import wraps
# from pathlib import Path
#
# from starlette.requests import Request
# # from token_sub_info.get_info import get_user_permissions
# # from token_sub_info.utils import get_token_from_request, validate_token
#
# from ..config import settings, method_to_function_map
# from ..exceptions.main_exceptions import ForbiddenException
# from ..exceptions.sub_exceptions.internal_exceptions import DebugModeNotFoundException
# from ..schemas.auth_schemas import AuthConfig, ParamSelection, DebugMode, MethodState
# from .utils import get_public_key
#
#
# function_to_method_map = {v: k for k, v in method_to_function_map.items()}
#
#
# def parse_auth() -> AuthConfig:
#     mode = None
#     methods = []
#
#     file_path = Path(settings.AUTH_PATH)
#
#     with open(file_path, 'r') as f:
#         for line in f:
#             line = line.strip()
#             if not line:
#                 continue
#             param = line.split("=")
#             if len(param) == 2:
#                 if param[0] == ParamSelection.DEBUG_MODE:
#                     mode = DebugMode(param[1])
#                 elif param[0] == ParamSelection.PERMISSIONS:
#                     methods.extend(param[1].split(","))
#
#     if not mode:
#         raise DebugModeNotFoundException
#
#     auth_config = AuthConfig()
#     auth_config.mode = mode
#     for method in methods:
#         method = method.strip()
#         if not method:
#             continue
#
#         if ":" in method:
#             method, state = method.split(':')
#             if state == "OPEN":
#                 auth_config.methods[method_to_function_map[method]] = MethodState.OPEN
#             elif state == "AUTHORIZED":
#                 auth_config.methods[method_to_function_map[method]] = MethodState.AUTHORIZED
#             elif state == "BLOCK":
#                 auth_config.methods[method_to_function_map[method]] = MethodState.BLOCKED
#         else:
#             auth_config.methods[method_to_function_map[method]] = MethodState.CLOSED
#
#     return auth_config
#
#
# # Декоратор для валидации прав
# def validate_permissions(func):
#     @wraps(func)
#     async def wrapper(request: Request, *args, **kwargs):
#         function = func.__name__
#         auth_config = request.app.state.auth_config
#
#         method_state = auth_config.methods.get(function)
#         if method_state == MethodState.BLOCKED or (auth_config.mode == DebugMode.PROD and method_state is None):
#             raise ForbiddenException
#
#         if method_state == MethodState.AUTHORIZED:
#             token = get_token_from_request(request)
#             validate_token(token, get_public_key(), settings.JWT_ALGORITHM)
#
#         if method_state == MethodState.CLOSED:
#             token = get_token_from_request(request)
#             user_permissions = get_user_permissions(token, get_public_key(), settings.JWT_ALGORITHM)
#             if not user_permissions or not user_permissions.get(settings.SERVICE_NAME) or \
#                     function_to_method_map[function].lower() not in user_permissions.get(settings.SERVICE_NAME):
#                 raise ForbiddenException
#
#         # Вызываем оригинальную функцию
#         response = await func(request, *args, **kwargs)
#         return response
#
#     return wrapper
