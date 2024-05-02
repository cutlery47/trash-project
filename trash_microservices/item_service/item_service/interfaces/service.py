from abc import ABC, abstractmethod

from item_service.interfaces.repository import RepositoryInterface

class ServiceInterface(ABC):
    @abstractmethod
    def __init__(self, repository: RepositoryInterface) -> None:
        raise NotImplementedError

    @abstractmethod
    async def do_shi(self, data):
        raise NotImplementedError
