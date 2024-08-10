from item_service.services.core.crud_service import CRUDService
from item_service.schemas.schemas.review_schema import ReviewAddDTO, ReviewDTO
from item_service.models.models import Review
from item_service.services.core.base_service import BaseReviewService
from item_service.repositories.repositories.repositories import ReviewRepository

from typing import Optional

from item_service.cache.core.base_cache_client import BaseCacheClient


class ReviewService(CRUDService[ReviewAddDTO, ReviewDTO], BaseReviewService):
    _entity_class = Review
    _dto_class = ReviewDTO
    _add_dto_class = ReviewAddDTO

    def __init__(self, repository: ReviewRepository, cache_client: Optional[BaseCacheClient] = None):
        super().__init__(repository, cache_client)
        self._repository = repository
        self._cache_client = cache_client

    async def get_by_user_id(self, user_id: int) -> list[ReviewDTO]:
        orm_data = await self._repository.get(self._entity_class.reviewer_id == user_id)
        return [self._dto_class.model_validate(data, from_attributes=True) for data in orm_data]

    async def get_by_item_id(self, item_id: int) -> list[ReviewDTO]:
        orm_data = await self._repository.get(self._entity_class.item_id == item_id)
        return [self._dto_class.model_validate(data, from_attributes=True) for data in orm_data]
