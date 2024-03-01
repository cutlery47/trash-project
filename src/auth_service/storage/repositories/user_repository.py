from pypika import Query, Table
import psycopg2

from .repository import Repository
from src.auth_service.storage.entities.entities import User
from src.auth_service.config.db_config import DBConfig


class UserRepository(Repository[User]):

    def __init__(self, user: User):
        self.user = user

        # connecting to db
        self.connection = psycopg2.connect(f"dbname={DBConfig.dbname} user={DBConfig.user}")
        self.cursor = self.connection.cursor()

    def __del__(self):
        self.cursor.close()
        self.connection.close()

    def get(self, id_: int) -> User:
        users = Table("users")

        q = Query.from_(users).select(
            users.id,
            users.role_id,
            users.email,
            users.password
        ).where(
            users.id == id_
        ).get_sql()
        self.cursor.execute(q)

        result = self.cursor.fetchone()

        # TODO: return column names as well in order to provide User class constructor with already mapped values

        # return User(
        #     {
        #         result[0]
        #     }
        # )


    def add(self, data: User) -> None:
        pass

    def delete(self, id_: int) -> None:
        pass

    def get_all(self) -> list[User]:
        pass

    def update(self, id_: int, data: User) -> None:
        pass
