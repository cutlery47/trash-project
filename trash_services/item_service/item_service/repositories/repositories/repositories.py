from item_service.repositories.core.crud_repository import CRUDRepository
from item_service.models.models import Category, Item, Review

from sqlalchemy.exc import SQLAlchemyError

class CategoryRepository(CRUDRepository[Category]):
    _entity_class = Category

class ItemRepository(CRUDRepository[Item]):
    _entity_class = Item

class ReviewRepository(CRUDRepository[Review]):
    _entity_class = Review

    async def create(self, review: Review) -> dict:
        async with self.sessionmaker() as session:
            try:
                session.add(review)
            except SQLAlchemyError as exc:
                await session.rollback()
                self.exc_handler.handle(exc)
            else:
                await session.commit()

                return {
                    "id": review.id,
                    "reviewed_at": review.reviewed_at
                }