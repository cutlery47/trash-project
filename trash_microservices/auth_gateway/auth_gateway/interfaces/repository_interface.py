from abc import ABC, abstractmethod

from auth_gateway.storage.entities.entities import User


class AuthRepositoryInterface(ABC):
    @abstractmethod
    def get(self, id_: int, secure: bool) -> User:
        raise NotImplementedError

    @abstractmethod
    def get_all(self, secure: bool) -> list[User]:
        raise NotImplementedError

    @abstractmethod
    def create(self, user_data: User) -> bool:
        raise NotImplementedError

    @abstractmethod
    def delete(self, id_: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    def update(self, id_: int, user_data: User) -> bool:
        raise NotImplementedError
