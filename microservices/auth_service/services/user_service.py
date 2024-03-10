import random

import psycopg2

from src.auth_service.storage.entities.entities import User


class UserService:

    def __init__(self, repo):
        self.repo = repo

    def get(self, id_: int):
        return self.repo.get(id_)

    def get_all(self):
        return self.repo.get_all()

    def create(self, user: User):
        user.id = self.randomize_id(1, 2 ** 31 - 1)
        user.role_id = 0
        return self.repo.create(user)

    def create_admin(self, admin: User):
        admin.id = self.randomize_id(1, 2 ** 31 - 1)
        admin.role_id = 1
        return self.repo.create(admin)

    def delete(self, id_):
        return self.repo.delete(id_)

    def update(self, id_, user: User):
        return self.repo.update(id_, user)

    def randomize_id(self, lower_bound: int, upper_bound: int):
        while True:
            id_ = random.randint(lower_bound, upper_bound)
            try:
                self.get(id_)
            except psycopg2.DataError:
                return id_
