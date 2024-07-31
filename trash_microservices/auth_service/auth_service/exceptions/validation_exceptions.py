from werkzeug.exceptions import HTTPException

class ValidationException(HTTPException):

    code = 400
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

class AdminRoleRequired(NotAllowedToAccessResource):

    description = "You should be admin to access the resource"
