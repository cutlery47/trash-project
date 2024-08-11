from fastapi import APIRouter, Request

from src.controller.handlers.validator import RequestValidator
from src.controller.core.base_controller import BaseController
from src.services.core.base_service import BaseService, BaseReviewService

from src.schemas.schemas.category_schema import CategoryAddDTO, CategoryDTO
from src.schemas.schemas.item_schema import ItemAddDTO, ItemDTO
from src.schemas.schemas.review_schema import ReviewAddDTO, ReviewDTO


class Controller(BaseController):

    def __init__(self,
                 item_service: BaseService,
                 review_service: BaseReviewService,
                 category_service: BaseService):

        self.item_service = item_service
        self.review_service = review_service
        self.category_service = category_service

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
        async def get_item(item_id: int) -> list[ItemDTO]:
            return await self.item_service.get(item_id)

        @self.router.post("/items/")
        async def add_item(item: ItemAddDTO) -> int:
            await self.item_service.create(item)
            return 200

        @self.router.delete("/items/{item_id}")
        async def delete_item(item_id: int) -> int:
            await self.item_service.delete(item_id)
            return 200

        @self.router.put("/items/{item_id}")
        async def update_item(item: ItemAddDTO, item_id: int) -> int:
            await self.item_service.update(item_id, item)
            return 200

        # ================= category api ========================

        @self.router.get("/categories/")
        async def get_categories() -> list[CategoryDTO]:
            return await self.category_service.get()

        @self.router.get("/categories/{category_id}")
        async def get_category(category_id: int) -> list[CategoryDTO]:
            return await self.category_service.get(category_id)

        @self.router.post("/categories/")
        async def add_category(category: CategoryAddDTO) -> int:
            await self.category_service.create(category)
            return 200

        @self.router.delete("/categories/{category_id}")
        async def delete_category(category_id: int) -> int:
            await self.category_service.delete(category_id)
            return 200

        @self.router.put("/categories/{category_id}")
        async def update_category(category_id: int, category: CategoryAddDTO) -> int:
            await self.category_service.update(category_id, category)
            return 200

        # ================= review api ========================

        @self.router.post("/reviews/")
        async def add_review(review: ReviewAddDTO) -> int:
            return await self.review_service.create(review)

        @self.router.get("/reviews/")
        async def get_reviews() -> list[ReviewDTO]:
            return await self.review_service.get()

        @self.router.get("/reviews/{review_id}")
        async def get_review(review_id: int) -> list[ReviewDTO]:
            return await self.review_service.get(review_id)

        @self.router.get("/reviews/items/{item_id}")
        async def get_item_reviews(item_id: int) -> list[ReviewDTO]:
            return await self.review_service.get_by_item_id(item_id)

        @self.router.get("/reviews/users/{user_id}")
        async def get_user_reviews(user_id: int) -> list[ReviewDTO]:
            return await self.review_service.get_by_user_id(user_id)

        @self.router.delete("/reviews/{review_id}")
        async def delete_review(review_id: int) -> int:
            await self.review_service.delete(review_id)
            return 200

        @self.router.put("/reviews/{review_id}")
        async def update_review(review_id: int, review: ReviewAddDTO) -> int:
            await self.review_service.update(review_id, review)
            return 200
