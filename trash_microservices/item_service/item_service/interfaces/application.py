from abc import ABC, abstractmethod

from item_service.interfaces.controller import ControllerInterface

from fastapi import FastAPI

# I fell like this one is redundant
# Might delete later
class ApplicationInterface(ABC):
    @abstractmethod
    def __init__(self, controller: ControllerInterface, config: dict) -> None:
        raise NotImplementedError

    @abstractmethod
    def asgi_app(self) -> FastAPI:
        """
        After initialization, you would create
        an entrypoint by calling this function
        :return: ASGI application, runnable by uvicorn
        """
        raise NotImplementedError
