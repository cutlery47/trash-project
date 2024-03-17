class ServiceException(Exception):
    pass


class PasswordDoNotMatchError(ServiceException):
    pass
