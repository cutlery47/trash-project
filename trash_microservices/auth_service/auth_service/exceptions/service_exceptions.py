class ServiceException(Exception):
    pass


class PasswordDoesNotMatchError(ServiceException):
    pass
