from item_service.interfaces.service import ServiceInterface
from item_service.interfaces.repository import RepositoryInterface
from item_service.schemas.review_schema import BaseReview, Review, ReviewAdd


class ReviewService(ServiceInterface[BaseReview]):
    def __init__(self, repository: RepositoryInterface):
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
