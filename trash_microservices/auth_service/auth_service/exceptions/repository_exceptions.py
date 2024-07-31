from werkzeug.exceptions import HTTPException

class RepositoryException(HTTPException):
    pass


class PostgresConnError(RepositoryException):
    pass


class UserNotFoundError(RepositoryException):
    pass


class FieldsNotProvidedError(RepositoryException):
    pass


class RoleNotFoundError(RepositoryException):
    pass


class PermissionsNotFoundError(RepositoryException):
    pass


class UniqueConstraintError(RepositoryException):
    pass
