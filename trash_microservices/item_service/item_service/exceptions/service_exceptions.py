from fastapi import HTTPException

class ServiceException(HTTPException):
    pass