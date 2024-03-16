from dataclasses import fields

from .entities import User


class UserSerializer:

    @staticmethod
    def serialize(entity: User) -> dict:
        res = dict()
        for el in fields(entity):
            attr = el.name
            attr_val = getattr(entity, el.name)
            if attr_val is not None:
                res[attr] = attr_val
        return res

    @staticmethod
    def deserialize(data: dict) -> User:
        return User(**data)
