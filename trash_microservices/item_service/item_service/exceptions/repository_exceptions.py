from fastapi.exceptions import HTTPException

class RepositoryException(HTTPException):
    pass

class DataNotFoundException(RepositoryException):
    def __init__(self, detail):
        self.status_code = 404
        self.detail = detail

class CreateNewRecordException(RepositoryException):
    def __init__(self, detail):
        self.status_code = 500
        self.detail = detail

class InternalRepositoryException(RepositoryException):
    def __init__(self, detail):
        self.status_code = 500
        self.detail = detail
