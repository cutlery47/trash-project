from fastapi import FastAPI

from item_service.interfaces.application import ApplicationInterface
from item_service.interfaces.router import RouterInterface

class Application(ApplicationInterface):
    def __init__(self, router: RouterInterface, config: dict):
        self.router = router
        self.app = FastAPI(**config)

    def asgi_app(self) -> FastAPI:
        return self.app
