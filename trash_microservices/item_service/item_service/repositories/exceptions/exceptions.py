from fastapi.exceptions import HTTPException
from starlette import status

class RepositoryException(HTTPException):
    pass

class DataNotFoundException(RepositoryException):
    def __init__(self):
        self.status_code = status.HTTP_404_NOT_FOUND
        self.detail = "Requested data was not found"

class InternalRepositoryException(RepositoryException):
    def __init__(self):
        self.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        self.detail = "An error occurred when processing your request"