from starlette.exceptions import HTTPException

class ValidationException(HTTPException):

    detail = "Provided data is invalid"

class RequiredFieldsNotProvided(ValidationException):

    status_code = 400

    def __init__(self, detail="Provided data is not sufficient to proceed"):
        self.detail = detail

class ForbiddenFieldsAreProvided(ValidationException):

    status_code = 400

    def __init__(self, detail="Provided data contains forbidden fields"):
        self.detail = detail

class TokenIsInvalid(ValidationException):

    status_code = 403
    detail = "Provided token is invalid"

    def __init__(self, detail):
        self.detail = f"{self.detail}: {detail}"

class NotAllowedToAccessResource(ValidationException):

    status_code = 403

    def __init__(self, detail="You are not allowed to access the resource"):
        self.detail = detail


class PasswordCantBeCreated(ValidationException):

    status_code = 400

    def __init__(self, detail: str = "Your password is invalid"):
        self.detail = detail


class EmailIsInvalid(ValidationException):

    status_code = 400

    def __init__(self, detail: str = "Provided email does not exist"):
        self.detail = detail
