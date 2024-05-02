from abc import ABC, abstractmethod

from item_service.interfaces.service import ServiceInterface


class ControllerInterface(ABC):
    @abstractmethod
    def __init__(self, service: ServiceInterface) -> None:
        raise NotImplementedError

    @abstractmethod
    async def do_shi(self, data):
        raise NotImplementedError
