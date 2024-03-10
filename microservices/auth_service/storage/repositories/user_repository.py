from pypika import Query, Table
from dataclasses import fields
import psycopg2

from .repository import Repository
from src.auth_service.storage.entities.entities import User
from src.auth_service.config.database.db_config import DBConfig


class UserRepository(Repository[User]):

    def __init__(self, db_config):
        # connecting to db
        config = DBConfig(db_config)
        self.connection = psycopg2.connect(f"dbname={config.dbname} user={config.user}")
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

        user_data = self.cursor.fetchone()
        if user_data:
            return User(*user_data)

        raise psycopg2.DataError("404: User was not found by specified id...")

    def get_all(self) -> list[User]:
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

        raise psycopg2.DataError("404: Users were not found...")

    def create(self, user_data: User) -> bool:
        users = Table("users")

        q = Query.into(users).insert(
            user_data.id,
            user_data.role_id,
            user_data.email,
            user_data.password
        ).get_sql()
        self.cursor.execute(q)
        self.connection.commit()

        # is used to check for any psql errors
        self.cursor.fetchone()

        return True

    def delete(self, id_: int) -> bool:
        users = Table("users")

        q = Query.from_(users).delete().where(
            users.id == id_
        ).get_sql()
        self.cursor.execute(q)
        self.connection.commit()

        # is used to check for any psql errors
        self.cursor.fetchall()

        return True

    def update(self, id_: int, user_data: User) -> bool:
        users = Table("Users")

        q = Query.update(users)
        for field in fields(User):
            field_val = getattr(user_data, field.name)
            if field_val is not None:
                q = q.set(field.name, field_val)
        q = q.get_sql()
        self.cursor.execute(q)
        self.connection.commit()

        # is used to check for any psql errors
        self.cursor.fetchone()

        return True
