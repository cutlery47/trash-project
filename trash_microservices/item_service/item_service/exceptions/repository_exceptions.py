from fastapi.exceptions import HTTPException

class RepositoryException(HTTPException):
    pass

class DataNotFoundException(RepositoryException):
    def __init__(self):
        self.status_code = 404
        self.detail = "Requested data was not found"

class InternalRepositoryException(RepositoryException):
    def __init__(self):
        self.status_code = 500
        self.detail = "An error occurred when processing your request"
