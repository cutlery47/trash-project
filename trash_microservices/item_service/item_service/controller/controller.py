from fastapi import APIRouter, Request

import httpx

from item_service.interfaces.base_controller import BaseController

from item_service.schemas.category_schema import CategoryAddDTO
from item_service.schemas.item_schema import ItemAddDTO, ItemDTO

from item_service.services.item_service import ItemService
from item_service.services.review_service import ReviewService
from item_service.services.category_service import CategoryService

from item_service.exceptions.controller_exceptions import AccessTokenInvalid, PermissionsDenied

from loguru import logger

class Controller(BaseController):

    def __init__(self,
                 item_service: ItemService,
                 review_service: ReviewService,
                 category_service: CategoryService,
                 urls: dict):
        self.item_service = item_service
        self.review_service = review_service
        self.category_service = category_service
        self.urls = urls

        self.router = APIRouter(prefix="/api/v1")
        self.setup_api()

    # Decided to make both methods below synchronous
    # because they are called only upon initialization
    # which means that them being sync won't affect
    # application runtime
    # IDK, maybe I'm horribly wrong for this

    def setup_api(self) -> None:
        @self.router.get("/items/")
        async def get_items(request: Request) -> list[ItemDTO]:
            await self.validate_access(request.cookies)
            return await self.item_service.get_all()

        @self.router.get("/items/{item_id}")
        async def get_item(request: Request, item_id: int) -> ItemDTO:
            await self.validate_access(cookies=request.cookies)
            return await self.item_service.get(item_id)

        @self.router.post("/items/add/")
        async def add_item(request: Request, item: ItemAddDTO) -> str:
            await self.validate_access_and_permissions(cookies=request.cookies,
                                                       user_id=item.merchant_id)
            await self.item_service.create(item)
            return "200"

        @self.router.delete("/items/{item_id}")
        async def delete_item(request: Request, item_id: int) -> str:
            item = await self.item_service.get(item_id)
            await self.validate_access_and_permissions(cookies=request.cookies,
                                                       user_id=item.merchant_id)
            await self.item_service.delete(item_id)
            return "200"

        @self.router.put("/items/{item_id}")
        async def update_item(request: Request, item: ItemAddDTO, item_id: int) -> str:
            await self.validate_access_and_permissions(cookies=request.cookies,
                                                       user_id=item.merchant_id)
            await self.item_service.update(item_id, item)
            return "200"

        @self.router.post("/categories/add/")
        async def add_category(category: CategoryAddDTO) -> None:
            await self.category_service.create(category)

    def get_api(self) -> APIRouter:
        return self.router

    async def validate_access(self, cookies: dict):
        re = httpx.post(url=self.urls['/validate/'], cookies=cookies)
        if re.status_code == 401:
            logger.error("Access token is invalid")
            raise AccessTokenInvalid

    async def validate_access_and_permissions(self, cookies: dict, user_id: int):
        re = httpx.post(url=self.urls['/validate/'] + str(user_id), cookies=cookies)
        if re.status_code == 401:
            logger.error("Access token is invalid")
            raise AccessTokenInvalid
        elif re.status_code == 403:
            logger.error("Permissions denied")
            raise PermissionsDenied
