from fastapi.applications import FastAPI, ASGIApp
from fastapi.testclient import TestClient

from httpx import AsyncClient, ASGITransport

from item_service.application.core.base_application import BaseApplication
from item_service.controller.core.base_controller import BaseController
from item_service.config.app.app_config import AppConfig

from dataclasses import asdict

class Application(BaseApplication):
    def __init__(self, controller: BaseController, config: AppConfig) -> None:
        self.asgi = FastAPI(**asdict(config))
        self.controller = controller
        self.asgi.include_router(self.controller.get_api())

    def asgi_app(self) -> ASGIApp:
        return self.asgi

    def test_client(self) -> TestClient:
        return TestClient(app=self.asgi_app(), follow_redirects=True)

    def async_test_client(self) -> AsyncClient:
        return AsyncClient(transport=ASGITransport(app=self.asgi_app()), follow_redirects=True)
