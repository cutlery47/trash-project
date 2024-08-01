from flask import Flask

from werkzeug.exceptions import HTTPException

from auth_service.exceptions.validation_exceptions import ValidationException, NotAllowedToAccessResource
from auth_service.exceptions.service_exceptions import ServiceException
from auth_service.exceptions.repository_exceptions import RepositoryException

def handle_exception(exc: Exception):
    return str(exc), 500


# Generic http exception handler
def handle_http_exception(exc: HTTPException):
    return exc.description, exc.code


def register_exception_handlers(app: Flask) -> None:

    # Unexpected exception handler
    app.register_error_handler(Exception, handle_exception)

    # Validation exception handlers
    app.register_error_handler(ValidationException, handle_http_exception)

    # Service exception handlers
    app.register_error_handler(ServiceException, handle_http_exception)

    # Repository exception handlers
    app.register_error_handler(RepositoryException, handle_http_exception)

