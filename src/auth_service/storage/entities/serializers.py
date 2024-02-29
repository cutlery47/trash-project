from builtins import classmethod
from dataclasses import asdict

from .entities import User


class UserSerializer:

    @classmethod
    def serialize(cls, data: dict) -> User:
        return User(**data)

    @classmethod
    def deserialize(cls, entity: User) -> dict:
        return asdict(entity)
