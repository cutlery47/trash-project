from pypika import Query, Table
from dataclasses import fields
import psycopg2

from .repository import Repository
from src.auth_service.storage.entities.entities import User
from src.auth_service.config.database.db_config import DBConfig


class UserRepository(Repository[User]):

    def __init__(self):
        # connecting to db
        self.connection = psycopg2.connect(f"dbname={DBConfig.dbname} user={DBConfig.user}")
        self.cursor = self.connection.cursor()

    def __del__(self):
        self.cursor.close()
        self.connection.close()

    def get(self, id_: int) -> User | str:
        users = Table("users")

        # iterating over each field of User entity
        user_fields = tuple(field.name for field in fields(User))

        q = Query.from_(users).select(
            *user_fields
        ).where(
            users.id == id_
        ).get_sql()
        self.cursor.execute(q)

        user_data = self.cursor.fetchone()

        if user_data:
            return User(*user_data)

        return "None"

    def get_all(self) -> list[User] | str:
        users = Table("users")

        # iterating over each field of User entity
        user_fields = tuple(field.name for field in fields(User))

        q = Query.from_(users).select(
            *user_fields
        ).get_sql()
        self.cursor.execute(q)

        users_data = self.cursor.fetchall()

        if users_data:
            return [User(*user_data) for user_data in users_data]
        else:
            return "None"

    def create(self, user_data: User) -> str:
        users = Table("users")

        q = Query.into(users).insert(
            user_data.id,
            user_data.role_id,
            user_data.email,
            user_data.password
        ).get_sql()
        self.cursor.execute(q)

        try:
            self.connection.commit()
        except psycopg2.DataError as err:
            return err.pgerror

        return "200"

    def delete(self, id_: int) -> str:
        pass

    def update(self, id_: int, data: User) -> str:
        pass
