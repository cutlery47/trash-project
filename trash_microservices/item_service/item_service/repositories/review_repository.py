from item_service.interfaces.repository import RepositoryInterface
from item_service.repositories.models.models import Review

from sqlalchemy.engine import Engine

class ReviewRepository(RepositoryInterface[Review]):
    def __init__(self, engine: Engine) -> None:
        self.engine = engine

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
