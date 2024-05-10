from abc import ABC, abstractmethod

from item_service.interfaces.base_controller import BaseController

from fastapi.applications import FastAPI, ASGIApp
from fastapi.testclient import TestClient


# I fell like this one is redundant
# Might delete later
class BaseApplication(ABC):
    @abstractmethod
    def __init__(self, controller: BaseController, config: dict) -> None:
        raise NotImplementedError

    @abstractmethod
    def asgi_app(self) -> ASGIApp:
        """
        After initialization, you would create
        an entrypoint by calling this function
        :return: ASGI application, runnable by uvicorn
        """
        raise NotImplementedError

    @abstractmethod
    def test_client(self) -> TestClient:
        """
        Returns a test client for testing purposes
        :return: TestClient instance
        """
        raise NotImplementedError
