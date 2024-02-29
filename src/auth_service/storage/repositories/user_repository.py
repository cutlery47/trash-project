from builtins import classmethod

from .repository import Repository
from ..entities.entities import User


class UserRepository(Repository[User]):
    user: User

    @classmethod
    def __init__(cls, user: User):
        cls.user = user

