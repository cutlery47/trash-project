from fastapi import APIRouter, Request

import requests

from item_service.interfaces.base_controller import BaseController

from item_service.schemas.category_schema import CategoryAddDTO
from item_service.schemas.item_schema import ItemAddDTO, ItemDTO

from item_service.services.item_service import ItemService
from item_service.services.review_service import ReviewService
from item_service.services.category_service import CategoryService

from item_service.exceptions.controller_exceptions import AccessTokenInvalid

from fastapi import Request

class Controller(BaseController):

    def __init__(self,
                 item_service: ItemService,
                 review_service: ReviewService,
                 category_service: CategoryService):
        self.item_service = item_service
        self.review_service = review_service
        self.category_service = category_service

        self.router = APIRouter(prefix="/api/v1")
        self.setup_api()

    # Decided to make both methods below synchronous
    # because they are called only upon initialization
    # which means that them being sync won't affect
    # application runtime
    # Idk, maybe I'm horribly wrong for this

    def setup_api(self) -> None:
        @self.router.get("/items/")
        async def get_items(request: Request) -> list[ItemDTO]:
            self.validate_access(request.cookies)
            return await self.item_service.get_all()


        @self.router.get("/items/{item_id}")
        async def get_item(request: Request, item_id: int) -> ItemDTO:
            self.validate_access(request.cookies)
            return await self.item_service.get(item_id)

        @self.router.post("/items/add/")
        async def add_item(request: Request, item: ItemAddDTO) -> str:
            self.validate_access(request.cookies)
            await self.item_service.create(item)
            return "200"

        @self.router.post("/categories/add/")
        async def add_category(category: CategoryAddDTO) -> None:
            await self.category_service.create(category)

    def get_api(self) -> APIRouter:
        return self.router

    def validate_access(self, cookies: dict):
        r = requests.post(url='http://127.0.0.1:9876/api/v1/validate/',
                          cookies=cookies)
        if r.status_code != 200:
            raise AccessTokenInvalid
