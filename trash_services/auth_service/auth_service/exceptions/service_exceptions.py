from werkzeug.exceptions import HTTPException

class ServiceException(HTTPException):

    description = "Unexpected error occurred when processing your request"


class PasswordDoesNotMatch(ServiceException):

    code = 403
    description = "Passwords do not match"



