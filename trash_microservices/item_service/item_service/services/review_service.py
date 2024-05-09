from item_service.interfaces.base_service import BaseService
from item_service.interfaces.base_repository import BaseRepository
from item_service.schemas.review_schema import BaseReviewDTO, ReviewDTO, ReviewAddDTO


class ReviewService(BaseService[BaseReviewDTO]):
    def __init__(self, repository: BaseRepository):
        self.repository = repository

    async def create(self, review: ReviewAddDTO) -> None:
        pass

    async def get(self, review_id: int) -> ReviewDTO:
        pass

    async def get_all(self) -> list[ReviewDTO]:
        pass

    async def update(self, review_id: int, review: ReviewAddDTO) -> None:
        pass

    async def delete(self, review_id: int) -> None:
        pass
