from pypika import Query, Table
from dataclasses import fields
import psycopg2

from auth_service.storage.entities.entities import User
from auth_service.config.database.db_config import DBConfig
from auth_service.storage.repositories.query_builder import QueryBuilder
from auth_service.interfaces.repository_interface import AuthRepositoryInterface

from auth_service.exceptions import repository_exceptions


# noinspection PyTypeChecker
class AuthRepository(AuthRepositoryInterface):

    def __init__(self, config: DBConfig, query_builder: QueryBuilder):
        self.query_builder = query_builder
        self.config = config

        # establishing db connection
        try:
            self.connection = psycopg2.connect(database=self.config.dbname, user=self.config.user, password=self.config.password)
        except psycopg2.Error:
            raise repository_exceptions.PostgresConnError("Couldn't establish database connection")

        self.cursor = self.connection.cursor()

    def get(self, secure: bool, id_: int = None, email: str = None) -> User:
        # iterating over each field of User entity
        if secure:
            user_fields = tuple(field.name for field in fields(User) if field.name != "password")
        else:
            user_fields = tuple(field.name for field in fields(User))

        users = Table("Users")
        if id_ is not None:
            q = self.query_builder.get(users, user_fields, users.id == id_)
        elif email is not None:
            q = self.query_builder.get(users, user_fields, users.email == email)
        else:
            raise repository_exceptions.FieldsNotProvidedError("Identification fields were not provided")

        self.cursor.execute(q)
        self.connection.commit()

        user_data = self.cursor.fetchone()
        if user_data:
            return User(*user_data)

        raise repository_exceptions.UserNotFoundError("User was not found by specified id")

    def get_all(self, secure: bool) -> list[User]:
        # iterating over each field of User entity
        if secure:
            user_fields = tuple(field.name for field in fields(User) if field.name != "password")
        else:
            user_fields = tuple(field.name for field in fields(User))

        users = Table("Users")
        q = self.query_builder.get(users, user_fields)

        self.cursor.execute(q)
        self.connection.commit()

        users_data = self.cursor.fetchall()
        return [User(*user_data) for user_data in users_data]

    def create(self, user_data: User) -> bool:
        users = Table("Users")
        user_fields = (user_data.id, user_data.role_id, user_data.email, user_data.password)
        q = self.query_builder.create(users, user_fields)

        try:
            self.cursor.execute(q)
        except psycopg2.IntegrityError:
            raise repository_exceptions.UniqueConstraintError("User with that email already exists")
        finally:
            self.connection.commit()

        return user_data.id

    def delete(self, id_: int) -> bool:
        users = Table("Users")
        q = self.query_builder.delete(users, users.id == id_)

        self.cursor.execute(q)
        self.connection.commit()

        # if number of affected fields = 0, => nothing was deleted
        if self.cursor.rowcount == 0:
            raise repository_exceptions.UserNotFoundError("User was not found by specified id")

        return True

    def update(self, id_: int, user_data: User) -> bool:
        users = Table("Users")
        user_fields = []

        # iterating over user_data and finding fields to change
        # the simply updating these fields with provided values
        for field in fields(User):
            field_val = getattr(user_data, field.name)
            if field_val is not None:
                user_fields.append((field.name, field_val))

        q = self.query_builder.update(users, user_fields, users.id == id_)

        self.cursor.execute(q)
        self.connection.commit()

        # if number of affected fields = 0, => nothing has updated
        if self.cursor.rowcount == 0:
            raise repository_exceptions.UserNotFoundError("User was not found by specified id")

        return True

    def get_role(self, id_: int) -> int:
        users = Table("Users")
        roles = Table("Roles")

        # single join:
        # joining Users with Roles according to role id
        q = Query.from_(users).left_join(
            roles
        ).on(users.role_id == roles.id).select(
            roles.name
        ).where(users.id == id_).get_sql()

        self.cursor.execute(q)
        self.connection.commit()

        role = self.cursor.fetchone()[0]
        if role is not None:
            return role

        raise repository_exceptions.RoleNotFoundError("Roles were not found for specified user")

    def get_permissions(self, id_) -> list[str]:
        users = Table("Users")
        role_permissions = Table("RolePermissions")
        permissions = Table("Permissions")

        # performing a double join:
        # 1) joining Users with Permissions, according to their roles
        # 2) joining User permissions with Permissions data
        q = Query.from_(users).join(role_permissions).on(
            users.role_id == role_permissions.role_id
        ).join(permissions).on(
            role_permissions.perm_id == permissions.id
        ).select(
            permissions.permission
        ).where(
            users.id == id_
        ).get_sql()

        self.cursor.execute(q)
        self.connection.commit()

        res = self.cursor.fetchall()
        if res is not None:
            return [record[0] for record in res]

        raise repository_exceptions.PermissionsNotFoundError("Permissions were not found for specified user")