from fastapi import HTTPException

class RepositoryException(HTTPException):

    detail = "Unexpected database error occurred when handling request"


class PostgresConnFailed(RepositoryException):

    status_code = 500

    def __init__(self, detail="Couldn't connect to the database"):
        self.detail = detail


class CriterionIsNotProvided(RepositoryException):

    status_code = 400

    def __init__(self, detail="Not sufficient data provided for building search criterion"):
        self.detail = detail



class DataNotFound(RepositoryException):

    status_code = 400
    detail = "Requested data was not found"

    def __init__(self, addit_detail: str):
        self.detail = self.detail + f": {addit_detail}"


class UniqueConstraintError(RepositoryException):

    status_code = 400
    detail = "The data already exists"

    def __init__(self, addit_detail: str):
        self.detail = self.detail + f": {addit_detail}"
