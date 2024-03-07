import random

from src.auth_service.storage.repositories.user_repository import UserRepository
from src.auth_service.storage.entities.entities import User


class UserService:

    def __init__(self):
        self.repo = UserRepository()

    def get(self, id_: int):
        return self.repo.get(id_)

    def get_all(self):
        return self.repo.get_all()

    def create(self, user: User):
        user.id = self.randomize_id(1, 2 ** 31 - 1)
        user.role_id = 0
        print(user)
        return self.repo.create(user)

    def create_admin(self, admin: User):
        admin.id = self.randomize_id(1, 2 ** 31 - 1)
        admin.role_id = 1
        print(admin)
        return self.repo.create(admin)

    def randomize_id(self, lower_bound: int, upper_bound: int):
        while True:
            id_ = random.randint(lower_bound, upper_bound)
            if not self.get(id_):
                return id_
