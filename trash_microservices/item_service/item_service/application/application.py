from fastapi.applications import FastAPI, ASGIApp
from fastapi.testclient import TestClient
from fastapi import Depends

from httpx import AsyncClient

from typing import Annotated

from item_service.interfaces.base_application import BaseApplication
from item_service.interfaces.base_controller import BaseController
from item_service.config.app_config import AppConfig

from dataclasses import asdict

class Application(BaseApplication):
    def __init__(self,
                 controller: Annotated[BaseController, Depends(get_contoller)],
                 config: Annotated[AppConfig, Depends(get_app_config)]
                 ):
        self.asgi = FastAPI(**asdict(config))
        self.controller = controller
        self.asgi.include_router(self.controller.get_api())

    def asgi_app(self) -> ASGIApp:
        return self.asgi

    def test_client(self) -> TestClient:
        return TestClient(app=self.asgi_app(), follow_redirects=True)

    def async_test_client(self) -> AsyncClient:
        return AsyncClient(app=self.asgi_app(), follow_redirects=True)
