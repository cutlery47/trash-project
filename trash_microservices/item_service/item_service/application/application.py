from fastapi import FastAPI

from item_service.interfaces.base_application import BaseApplication
from item_service.interfaces.base_controller import BaseController
from item_service.config.app_config import AppConfig

from dataclasses import asdict

class Application(BaseApplication):
    def __init__(self, controller: BaseController, config: AppConfig) -> None:
        self.asgi = FastAPI(**asdict(config))
        self.controller = controller
        self.asgi.include_router(self.controller.get_api())

    def asgi_app(self) -> FastAPI:
        return self.asgi
