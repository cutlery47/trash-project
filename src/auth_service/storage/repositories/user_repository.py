from pypika import Query, Table
from dataclasses import fields
import psycopg2

from .repository import Repository
from src.auth_service.storage.entities.entities import User
from src.auth_service.config.db_config import DBConfig


class UserRepository(Repository[User]):

    def __init__(self):
        # connecting to db
        self.connection = psycopg2.connect(f"dbname={DBConfig.dbname} user={DBConfig.user}")
        self.cursor = self.connection.cursor()

    def __del__(self):
        self.cursor.close()
        self.connection.close()

    def get(self, id_: int) -> User:
        users = Table("users")

        # iterating over each field of User entity
        user_fields = tuple(field.name for field in fields(User))

        q = Query.from_(users).select(
            *user_fields
        ).where(
            users.id == id_
        ).get_sql()
        self.cursor.execute(q)

        result = self.cursor.fetchone()

        if result:
            return User(*result)
        else:
            return User()

    def add(self, data: User) -> None:
        pass

    def delete(self, id_: int) -> None:
        pass

    def get_all(self) -> list[User]:
        pass

    def update(self, id_: int, data: User) -> None:
        pass
