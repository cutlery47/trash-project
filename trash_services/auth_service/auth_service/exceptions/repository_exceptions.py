from werkzeug.exceptions import HTTPException

class RepositoryException(HTTPException):

    description = "Unexpected database error occurred when handling request"


class PostgresConnFailed(RepositoryException):

    code = 500
    description = "Couldn't connect to the database"

class CriterionIsNotProvided(RepositoryException):

    code = 400
    description = "Not sufficient data provided for building search criterion"


class DataNotFound(RepositoryException):

    code = 400
    description = "Requested data was not found"

    def __init__(self, addit_description: str):
        self.description = self.description + f": {addit_description}"


class UniqueConstraintError(RepositoryException):

    code = 400
    description = "The data already exists"

    def __init__(self, addit_description: str):
        self.description = self.description + f": {addit_description}"
