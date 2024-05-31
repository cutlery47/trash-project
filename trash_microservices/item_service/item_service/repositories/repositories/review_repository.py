from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, AsyncSession

from item_service.repositories.core.crud_repository import CRUDRepository
from item_service.models.models import Review
from item_service.repositories.handlers.exception_handler import RepositoryExceptionHandler


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
