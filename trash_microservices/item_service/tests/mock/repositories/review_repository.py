from item_service.interfaces.base_repository import BaseRepository
from item_service.repositories.models.models import Review
from item_service.exceptions.repository_exceptions import DataNotFoundException


class MockReviewRepository(BaseRepository[Review]):
    def __init__(self):
        self.db = []

    def create(self, review: Review) -> None:
        review.id = len(self.db) + 1
        self.db.append(review.__dict__)

    def get(self, _id: int) -> Review:
        for el in self.db:
            if el['id'] == _id:
                return Review(**el)
        raise DataNotFoundException

    def get_all(self) -> list[Review]:
        return [Review(**data) for data in self.db]

    def delete(self, _id: int) -> None:
        pass

    def update(self, _id: int, review: Review) -> None:
        pass
