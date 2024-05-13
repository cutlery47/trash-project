from item_service.interfaces.base_repository import BaseRepository
from item_service.repositories.models.models import Review

from sqlalchemy.engine import Engine
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine, async_sessionmaker

class ReviewRepository(BaseRepository[Review]):
    def __init__(self, engine: AsyncEngine, sessionmaker: async_sessionmaker[AsyncSession]) -> None:
        self.engine = engine
        self.sessionmaker = sessionmaker

    async def create(self, review: Review) -> Review:
        pass

    async def get(self, review_id: Review) -> Review:
        pass

    async def get_all(self) -> list[Review]:
        pass

    async def update(self, review_id: int, review: Review) -> Review:
        pass

    async def delete(self, review_id: int):
        pass
