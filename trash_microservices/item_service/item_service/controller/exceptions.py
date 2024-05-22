from fastapi import HTTPException
from starlette import status

from loguru import logger


class ControllerException(HTTPException):
    pass

class HttpMethodNotAllowed(ControllerException):
    def __init__(self):
        self.status_code = status.HTTP_405_METHOD_NOT_ALLOWED
        self.detail = "Method not allowed"

class AccessTokenInvalid(ControllerException):
    def __init__(self):
        self.status_code = status.HTTP_401_UNAUTHORIZED
        self.detail = "Invalid access token"

class PermissionsDenied(ControllerException):
    def __init__(self):
        self.status_code = status.HTTP_403_FORBIDDEN
        self.detail = "Permission denied"

class ResourceAccessDenied(ControllerException):
    def __init__(self):
        self.status_code = status.HTTP_403_FORBIDDEN
        self.detail = "Resource access denied"
