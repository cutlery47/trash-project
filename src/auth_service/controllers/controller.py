from abc import ABC, abstractmethod
from flask import Request


class Controller[Entity](ABC):
    entity: Entity

    @abstractmethod
    def __init__(self, request):
        raise NotImplementedError

    @abstractmethod
    def handle_get(self, id_: int):
        raise NotImplementedError

    @abstractmethod
    def handle_get_all(self):
        raise NotImplementedError

    @abstractmethod
    def _integrity_check(self):
        raise NotImplementedError



