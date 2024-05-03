from fastapi import APIRouter

from item_service.interfaces.service import ServiceInterface
from item_service.interfaces.controller import ControllerInterface

class Controller(ControllerInterface):

    def __init__(self,
                 item_service: ServiceInterface,
                 review_service: ServiceInterface,
                 category_service: ServiceInterface):
        self.item_service = item_service
        self.review_service = review_service
        self.category_service = category_service

        self.router = APIRouter()
        self.setup_api()

    # Decided to make both methods below synchronous
    # because they are called only upon initialization
    # which means that them being sync won't affect
    # application runtime
    # Idk, maybe I'm horribly wrong for this

    def setup_api(self) -> None:
        @self.router.get("/items/")
        async def get_items():
            return await self.item_service.get_all()

    def get_api(self) -> APIRouter:
        return self.router
