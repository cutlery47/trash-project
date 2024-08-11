from fastapi import HTTPException
from starlette import status

from loguru import logger


class ControllerException(HTTPException):
    pass

class HttpMethodNotAllowed(ControllerException):
    status_code = status.HTTP_405_METHOD_NOT_ALLOWED

    def __init__(self, detail="Method not allowed"):
        self.detail = detail

class AccessTokenInvalid(ControllerException):
    status_code = status.HTTP_401_UNAUTHORIZED

    def __init__(self, detail="Invalid access token"):
        self.detail = detail

class PermissionsDenied(ControllerException):
    status_code = status.HTTP_403_FORBIDDEN

    def __init__(self, detail="Permission denied"):
        self.detail = detail

class ResourceAccessDenied(ControllerException):
    status_code = status.HTTP_403_FORBIDDEN

    def __init__(self):
        self.detail = "Resource access denied"
