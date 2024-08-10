from starlette.exceptions import HTTPException

class ServiceException(HTTPException):

    detail = "Unexpected error occurred when processing your request"


class PasswordDoesNotMatch(ServiceException):

    status_code = 403

    def __init__(self, detail="Passwords do not match"):
        self.detail = detail



