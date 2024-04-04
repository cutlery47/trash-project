class RepositoryError(Exception):
    pass


class PostgresConnError(RepositoryError):
    pass


class UserNotFoundError(RepositoryError):
    pass


class FieldsNotProvidedError(RepositoryError):
    pass


class RoleNotFoundError(RepositoryError):
    pass


class PermissionsNotFoundError(RepositoryError):
    pass


class UniqueConstraintError(RepositoryError):
    pass
