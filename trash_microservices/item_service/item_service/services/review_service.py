from item_service.interfaces.base_service import BaseService
from item_service.interfaces.base_repository import BaseRepository
from item_service.schemas.review_schema import BaseReviewDTO, ReviewDTO, ReviewAddDTO
from item_service.repositories.models.models import Review

from typing import Annotated

from fastapi import Depends


class ReviewService(BaseService[BaseReviewDTO]):
    def __init__(self,
                 repository: Annotated[BaseRepository[Review], Depends(get_crud_repository, use_cache=False)]):
        self.repository = repository

    async def create(self, review: ReviewAddDTO) -> None:
        orm_review = Review(**review.model_dump())
        await self.repository.create(entity=orm_review)

    async def get(self, review_id: int) -> ReviewDTO:
        orm_review = await self.repository.get(review_id)
        return ReviewDTO.model_validate(orm_review, from_attributes=True)

    async def get_all(self) -> list[ReviewDTO]:
        orm_reviews = await self.repository.get()
        return [ReviewDTO.model_validate(orm_review, from_attributes=True) for orm_review in orm_reviews]

    async def get_all_for_item(self, item_id: int) -> list[ReviewDTO]:
        orm_reviews = await self.repository.get_all_for_item(item_id)
        return [ReviewDTO.model_validate(orm_review, from_attributes=True) for orm_review in orm_reviews]

    async def update(self, review_id: int, review: ReviewAddDTO) -> None:
        orm_review = Review(**review.model_dump())
        await self.repository.update(entity_id=review_id, entity=orm_review)

    async def delete(self, review_id: int) -> None:
        await self.repository.delete(review_id)
