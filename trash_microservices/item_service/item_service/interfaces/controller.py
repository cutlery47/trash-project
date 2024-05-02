from abc import ABC, abstractmethod

from item_service.interfaces.service import ServiceInterface


class ControllerInterface(ABC):
    @abstractmethod
    def __init__(self, service: ServiceInterface):
        raise NotImplementedError

    @abstractmethod
    def do_shi(self, data):
        raise NotImplementedError
