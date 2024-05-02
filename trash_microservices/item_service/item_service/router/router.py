from item_service.interfaces.router import RouterInterface
from item_service.interfaces.controller import ControllerInterface

from fastapi import APIRouter


class Router(RouterInterface):

    def __init__(self, controller: ControllerInterface) -> None:
        self.controller = controller
        self.api_router = APIRouter()
        self.setup_api()

    # if you wonder why below methods are sync --
    # feel free to read RouterInterface explanation

    def setup_api(self) -> None:
        @self.api_router.get("/")
        def xyu():
            return "123131"

    def get_api(self) -> APIRouter:
        return self.api_router
