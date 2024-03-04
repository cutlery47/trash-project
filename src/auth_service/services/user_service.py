from src.auth_service.storage.repositories.user_repository import UserRepository


class UserService:

    def __init__(self):
        self.repo = UserRepository()

    def get(self, id_: int):
        return self.repo.get(id_)

    def get_all(self):
        return self.repo.get_all()

