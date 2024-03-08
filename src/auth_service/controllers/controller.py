from abc import ABC, abstractmethod
from flask import Response


class Controller[Entity](ABC):

    @abstractmethod
    def __init__(self, request):
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



