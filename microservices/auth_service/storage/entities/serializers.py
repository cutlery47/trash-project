from dataclasses import asdict

from .entities import User


class UserSerializer:

    @staticmethod
    def serialize(data: dict) -> User:
        return User(**data)

    @staticmethod
    def deserialize(entity: User) -> dict:
        return asdict(entity)
