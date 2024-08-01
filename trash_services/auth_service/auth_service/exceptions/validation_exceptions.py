from werkzeug.exceptions import HTTPException

class ValidationException(HTTPException):

    description = "Provided data is invalid"

class RequiredFieldsNotProvided(ValidationException):

    code = 400
    description = "Provided data is not sufficient to proceed"

    def __init__(self, description):
        self.description = description

class ForbiddenFieldsAreProvided(ValidationException):

    code = 400
    description = "Provided data contains forbidden fields"

    def __init__(self, description):
        self.description = description

class TokenIsInvalid(ValidationException):

    code = 403
    description = "Provided token is invalid"

    def __init__(self, description):
        self.description = f"{self.description}: {description}"

class NotAllowedToAccessResource(ValidationException):

    code = 403
    description = "You are not allowed to access the resource"

    def __init__(self, description):
        self.description = description


class PasswordCantBeCreated(ValidationException):

    code = 400
    description = "Your password is invalid"

    def __init__(self, description: str):
        self.description = description


class EmailIsInvalid(ValidationException):

    code = 400
    description = "Provided email does not exist"

    def __init__(self, description: str):
        self.description = description
