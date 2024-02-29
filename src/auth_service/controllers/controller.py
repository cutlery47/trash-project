from abc import ABC, abstractmethod
from flask import Request


class Controller(ABC):
    desired_keys: list
    request: Request
    data: dict

    @abstractmethod
    def __init__(self, request):
        raise NotImplementedError

    @abstractmethod
    def _integrity_check(self):
        raise NotImplementedError

    @abstractmethod
    def handle(self):
        raise NotImplementedError

