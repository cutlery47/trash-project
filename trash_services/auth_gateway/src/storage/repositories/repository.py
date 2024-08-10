from pypika import Table
from dataclasses import fields
import psycopg2

from src.storage.entities.entities import User
from src.config.database.db_config import DBConfig
from src.storage.repositories.query_builder import CRUDQueryBuilder
from src.interfaces.repository_interface import AuthRepositoryInterface

from src.exceptions.repository_exceptions import *


# noinspection PyTypeChecker,SqlResolve
class AuthRepository(AuthRepositoryInterface):

    def __init__(self, config: DBConfig, query_builder: CRUDQueryBuilder):
        self.query_builder = query_builder
        self.config = config

        # establishing db connection
        try:
            self.connection = psycopg2.connect(database=self.config.dbname,
                                               user=self.config.user,
                                               password=self.config.password)
        except psycopg2.Error:
            raise PostgresConnFailed()

        self.cursor = self.connection.cursor()

    def create(self, user_data: User) -> bool:

        users = Table("users")
        user_fields = (user_data.id, user_data.role, user_data.email, user_data.password)
        q = self.query_builder.create(users, user_fields)

        try:
            self.cursor.execute(q)
        except psycopg2.IntegrityError:
            raise UniqueConstraintError("User with that email already exists")
        finally:
            self.connection.commit()

        return user_data.id

    def get(self, is_secure: bool, id_: int = None, email: str = None) -> User:

        # iterating over each field of User entity
        if is_secure:
            user_fields = tuple(field.name for field in fields(User) if field.name != "password")
        else:
            user_fields = tuple(field.name for field in fields(User))

        users = Table("users")
        if id_ is not None:
            q = self.query_builder.read(users, user_fields, users.id == id_)
        elif email is not None:
            q = self.query_builder.read(users, user_fields, users.email == email)
        else:
            raise CriterionIsNotProvided()

        self.cursor.execute(q)
        self.connection.commit()

        user_data = self.cursor.fetchone()
        if user_data:
            return User(*user_data)

        raise DataNotFound("Such user does not exist")

    def get_all(self, is_secure: bool) -> list[User]:

        # iterating over each field of User entity
        if is_secure:
            user_fields = tuple(field.name for field in fields(User) if field.name != "password")
        else:
            user_fields = tuple(field.name for field in fields(User))

        users = Table("users")
        q = self.query_builder.read(users, user_fields)

        self.cursor.execute(q)
        self.connection.commit()

        users_data = self.cursor.fetchall()
        return [User(*user_data) for user_data in users_data]

    def delete(self, id_: int):

        users = Table("users")
        q = self.query_builder.delete(users, users.id == id_)

        self.cursor.execute(q)
        self.connection.commit()

        # if number of affected fields = 0, => nothing was deleted
        if self.cursor.rowcount == 0:
            raise DataNotFound("User was not found by specified id")


    def update(self, id_: int, user_data: User):

        users = Table("users")
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
            raise DataNotFound("User was not found by specified id")

    def exists(self, id_: int) -> bool:
        return self.cursor.execute(f"SELECT EXISTS(SELECT 1 FROM users WHERE id={id_})")
