from abc import ABC, abstractmethod

from item_service.interfaces.repository import RepositoryInterface

class ServiceInterface(ABC):
    @abstractmethod
    def __init__(self, repository: RepositoryInterface):
        raise NotImplementedError

    @abstractmethod
    def do_shi(self, data):
        raise NotImplementedError
