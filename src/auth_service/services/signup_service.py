from builtins import classmethod

from src.auth_service.storage.entities.entities import User, Role
from src.auth_service.storage.entities.serializers import UserSerializer
from src.auth_service.storage.repositories.user_repository import UserRepository


class SignUpService:

    @classmethod
    def handle(cls, data: dict):
        user = UserSerializer.serialize(data)
        UserRepository(user).get(123123)
        return "123123"
