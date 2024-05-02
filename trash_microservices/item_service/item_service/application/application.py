from fastapi import FastAPI

from item_service.interfaces.application import ApplicationInterface
from item_service.interfaces.router import RouterInterface

class Application(ApplicationInterface):
    def __init__(self, router: RouterInterface, config: dict) -> None:
        self.app = FastAPI(**config)
        self.router = router
        self.app.include_router(self.router.get_api())

    def asgi_app(self) -> FastAPI:
        return self.app
