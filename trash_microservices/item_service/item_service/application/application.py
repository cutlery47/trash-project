from fastapi import FastAPI

from item_service.interfaces.application import ApplicationInterface
from item_service.interfaces.controller import ControllerInterface

class Application(ApplicationInterface):
    def __init__(self, controller: ControllerInterface, config: dict) -> None:
        self.asgi = FastAPI(**config)
        self.controller = controller
        self.asgi.include_router(self.controller.get_api())

    def asgi_app(self) -> FastAPI:
        return self.asgi
