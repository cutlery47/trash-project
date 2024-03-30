class ServiceException(Exception):
    pass


class PasswordDoesNotMatchError(ServiceException):
    pass


class TokenException(Exception):
    pass


class TokenIsInvalid(TokenException):
    pass


class PasswordException(Exception):
    pass


class PasswordLengthExceededError(PasswordException):
    pass


class PasswordLengthInsufficientError(PasswordException):
    pass


class PasswordHasNoDigitsError(PasswordException):
    pass


class PasswordHasNoLettersError(PasswordException):
    pass


class PasswordHasSpaceSeparatorError(PasswordException):
    pass


class EmailException(Exception):
    pass
