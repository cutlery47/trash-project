class RepositoryError(Exception):
    pass


class PostgresConnError(RepositoryError):
    pass


class UserNotFoundError(RepositoryError):
    pass


class RoleNotFound(RepositoryError):
    pass


class PermissionsNotFoundError(RepositoryError):
    pass


class UniqueConstraintError(RepositoryError):
    pass
