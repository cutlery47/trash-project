from abc import ABC, abstractmethod

from item_service.interfaces.router import RouterInterface

# I fell like this one is redundant
# Might delete later
class ApplicationInterface(ABC):
    @abstractmethod
    def __init__(self, router: RouterInterface, config: dict):
        raise NotImplementedError

    @abstractmethod
    def asgi_app(self):
        raise NotImplementedError
