from fastapi import APIRouter, Request, Response

import httpx

from item_service.interfaces.base_controller import BaseController

from item_service.schemas.category_schema import CategoryAddDTO, CategoryDTO
from item_service.schemas.item_schema import ItemAddDTO, ItemDTO
from item_service.schemas.review_schema import ReviewAddDTO, ReviewDTO

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

    def get_api(self) -> APIRouter:
        return self.router

    # Decided to make both methods below synchronous
    # because they are called only upon initialization
    # which means that them being sync won't affect
    # application runtime
    # IDK, maybe I'm horribly wrong for this

    def setup_api(self) -> None:
        # ================= item api ========================

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

        # ================= category api ========================

        @self.router.get("/categories/")
        async def get_categories(request: Request) -> list[CategoryDTO]:
            await self.validate_access(request.cookies)
            return await self.category_service.get_all()

        @self.router.get("/categories/{category_id}")
        async def get_category(request: Request, category_id: int) -> CategoryDTO:
            await self.validate_access(request.cookies)
            return await self.category_service.get(category_id)

        @self.router.post("/categories/")
        async def add_category(request: Request, category: CategoryAddDTO) -> str:
            await self.validate_access(request.cookies)
            await self.category_service.create(category)
            return "200"

        @self.router.delete("/categories/{category_id}")
        async def delete_category(request: Request, category_id: int) -> str:
            await self.validate_access(request.cookies)
            await self.category_service.delete(category_id)
            return "200"

        @self.router.put("/categories/{category_id}")
        async def update_category(request: Request, category_id: int, category: CategoryAddDTO) -> str:
            await self.validate_access_and_permissions(request.cookies)
            await self.category_service.update(category_id, category)
            return "200"

        # ================= review api ========================

        @self.router.get("/reviews/")
        async def get_reviews(request: Request) -> list[ReviewDTO]:
            await self.validate_access(request.cookies)
            reviews = await self.review_service.get_all()
            return reviews

        @self.router.get("/reviews/{review_id}")
        async def get_review(request: Request, review_id: int) -> ReviewDTO:
            await self.validate_access(request.cookies)
            review = await self.review_service.get(review_id)
            return review

        @self.router.get("/reviews/{item_id}")
        async def get_item_reviews(request: Request, item_id: int) -> list[ReviewDTO]:
            await self.validate_access(request.cookies)
            reviews = await self.review_service.get_item_all(item_id)
            return reviews

        @self.router.post("/reviews/add/")
        async def add_review(request: Request, review: ReviewAddDTO) -> str:
            await self.validate_access_and_permissions(request.cookies,
                                                       user_id=review.reviewer_id)
            await self.review_service.create(review)
            return "200"

        @self.router.delete("/reviews/{review_id}")
        async def delete_review(request: Request, review_id: int) -> str:
            review = await self.review_service.get(review_id)
            await self.validate_access_and_permissions(cookies=request.cookies,
                                                       user_id=review.reviewer_id)
            await self.review_service.delete(review_id)
            return "200"

        @self.router.put("/reviews/{review_id}")
        async def update_review(request: Request, review_id: int, review: ReviewAddDTO) -> str:
            await self.validate_access_and_permissions(request.cookies,
                                                       user_id=review.reviewer_id)
            await self.review_service.update(review_id, review)
            return "200"

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
