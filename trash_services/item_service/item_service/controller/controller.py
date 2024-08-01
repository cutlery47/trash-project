from fastapi import APIRouter, Request

from item_service.controller.handlers.validator import RequestValidator
from item_service.controller.core.base_controller import BaseController
from item_service.services.core.base_service import BaseService, BaseReviewService

from item_service.schemas.schemas.category_schema import CategoryAddDTO, CategoryDTO
from item_service.schemas.schemas.item_schema import ItemAddDTO, ItemDTO
from item_service.schemas.schemas.review_schema import ReviewAddDTO, ReviewDTO


class Controller(BaseController):

    def __init__(self,
                 item_service: BaseService,
                 review_service: BaseReviewService,
                 category_service: BaseService,
                 request_validator: RequestValidator):
        self.item_service = item_service
        self.review_service = review_service
        self.category_service = category_service
        self.validator = request_validator

        self.router = APIRouter(prefix="/api/v1")
        self.setup_api()

    def get_api(self) -> APIRouter:
        return self.router

    def setup_api(self) -> None:

        # ================= item api ========================

        @self.router.get("/items/")
        async def get_items(request: Request) -> list[ItemDTO]:
            return await self.item_service.get()

        @self.router.get("/items/{item_id}")
        async def get_item(request: Request, item_id: int) -> list[ItemDTO]:
            return await self.item_service.get(item_id)

        @self.router.post("/items/")
        async def add_item(request: Request, item: ItemAddDTO) -> int:
            await self.validator.validate_access_and_id(user_id=item.merchant_id, cookies=request.cookies)
            return await self.item_service.create(item)

        @self.router.delete("/items/{item_id}")
        async def delete_item(request: Request, item_id: int) -> int:
            item = await self.item_service.get(item_id)
            await self.validator.validate_access_and_id(cookies=request.cookies, user_id=item[0].merchant_id)
            await self.item_service.delete(item_id)
            return 200

        @self.router.put("/items/{item_id}")
        async def update_item(request: Request, item: ItemAddDTO, item_id: int) -> int:
            await self.validator.validate_access_and_id(cookies=request.cookies, user_id=item.merchant_id)
            await self.item_service.update(item_id, item)
            return 200

        # ================= category api ========================

        @self.router.get("/categories/")
        async def get_categories(request: Request) -> list[CategoryDTO]:
            await self.validator.validate_access(cookies=request.cookies)
            return await self.category_service.get()

        @self.router.get("/categories/{category_id}")
        async def get_category(request: Request, category_id: int) -> list[CategoryDTO]:
            await self.validator.validate_access(cookies=request.cookies)
            return await self.category_service.get(category_id)

        @self.router.post("/categories/")
        async def add_category(request: Request, category: CategoryAddDTO) -> int:
            await self.validator.validate_access(cookies=request.cookies)
            return await self.category_service.create(category)

        @self.router.delete("/categories/{category_id}")
        async def delete_category(request: Request, category_id: int) -> int:
            await self.validator.validate_access_and_admin(cookies=request.cookies)
            await self.category_service.delete(category_id)
            return 200

        @self.router.put("/categories/{category_id}")
        async def update_category(request: Request, category_id: int, category: CategoryAddDTO) -> int:
            await self.validator.validate_access_and_admin(cookies=request.cookies)
            await self.category_service.update(category_id, category)
            return 200

        # ================= review api ========================

        @self.router.post("/reviews/")
        async def add_review(request: Request, review: ReviewAddDTO) -> int:
            await self.validator.validate_access_and_id(cookies=request.cookies, user_id=review.reviewer_id)
            return await self.review_service.create(review)

        @self.router.get("/reviews/")
        async def get_reviews(request: Request) -> list[ReviewDTO]:
            await self.validator.validate_access(cookies=request.cookies)
            return await self.review_service.get()

        @self.router.get("/reviews/{review_id}")
        async def get_review(request: Request, review_id: int) -> list[ReviewDTO]:
            await self.validator.validate_access(cookies=request.cookies)
            return await self.review_service.get(review_id)

        @self.router.get("/reviews/items/{item_id}")
        async def get_item_reviews(request: Request, item_id: int) -> list[ReviewDTO]:
            await self.validator.validate_access(cookies=request.cookies)
            return await self.review_service.get_by_item_id(item_id)

        @self.router.get("/reviews/users/{user_id}")
        async def get_user_reviews(request: Request, user_id: int) -> list[ReviewDTO]:
            await self.validator.validate_access(cookies=request.cookies)
            return await self.review_service.get_by_user_id(user_id)

        @self.router.delete("/reviews/{review_id}")
        async def delete_review(request: Request, review_id: int) -> int:
            review = await self.review_service.get(review_id)
            await self.validator.validate_access_and_id(cookies=request.cookies, user_id=review[0].reviewer_id)
            await self.review_service.delete(review_id)
            return 200

        @self.router.put("/reviews/{review_id}")
        async def update_review(request: Request, review_id: int, review: ReviewAddDTO) -> int:
            await self.validator.validate_access_and_id(cookies=request.cookies, user_id=review.reviewer_id)
            await self.review_service.update(review_id, review)
            return 200
