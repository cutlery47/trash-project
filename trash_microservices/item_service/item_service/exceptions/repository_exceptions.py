from fastapi.exceptions import HTTPException

class RepositoryException(HTTPException):
    pass

class ResourceNotFoundException(HTTPException):
    def __init__(self, detail):
        self.status_code = 404
        self.detail = detail