from abc import ABC, abstractmethod
from flask import Response

from microservices.auth_service.services.user_service import UserService


class Controller[Entity](ABC):

    @abstractmethod
    def __init__(self, service: UserService):
        raise NotImplementedError

    @abstractmethod
    def get(self, id_: int) -> Response:
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> Response:
        raise NotImplementedError

    @abstractmethod
    def create(self) -> Response:
        raise NotImplementedError

    @abstractmethod
    def create_admin(self) -> Response:
        raise NotImplementedError

    @abstractmethod
    def delete(self, user_id) -> Response:
        raise NotImplementedError

    @abstractmethod
    def update(self, user_id) -> Response:
        raise NotImplementedError



