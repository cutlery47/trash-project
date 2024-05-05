from item_service.interfaces.base_service import BaseService
from item_service.schemas.review_schema import BaseReview, Review, ReviewAdd
from item_service.repositories.review_repository import ReviewRepository


class ReviewService(BaseService[BaseReview]):
    def __init__(self, repository: ReviewRepository):
        self.repository = repository

    async def create(self, review: ReviewAdd) -> None:
        pass

    async def get(self, review_id: int) -> Review:
        pass

    async def get_all(self) -> list[Review]:
        pass

    async def update(self, review_id: int, review: ReviewAdd) -> None:
        pass

    async def delete(self, review_id: int) -> None:
        pass
