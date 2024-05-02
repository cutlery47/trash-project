from abc import ABC, abstractmethod

from item_service.interfaces.controller import ControllerInterface


class RouterInterface(ABC):
    @abstractmethod
    def __init__(self, controller: ControllerInterface):
        raise NotImplementedError

    @abstractmethod
    def set_routes(self):
        raise NotImplementedError
