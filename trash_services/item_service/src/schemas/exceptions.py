from fastapi import HTTPException
from starlette import status

class SchemaException(HTTPException):
    pass

class FieldValidationException(SchemaException):
    def __init__(self, detail):
        self.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        self.detail = detail
