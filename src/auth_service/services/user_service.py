from builtins import classmethod

from src.auth_service.storage.entities.entities import User, Role
from src.auth_service.storage.entities.serializers import UserSerializer
from src.auth_service.storage.repositories.user_repository import UserRepository


class UserService:

    @classmethod
    def get(cls, id_: int):
        repo = UserRepository()
        return repo.get(id_)

