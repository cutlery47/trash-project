from item_service.interfaces.base_repository import BaseRepository
from item_service.repositories.models.models import Category
from item_service.exceptions.repository_exceptions import DataNotFoundException

class MockCategoryRepository(BaseRepository[Category]):
    def __init__(self):
        self.db = []

    def create(self, category: Category) -> None:
        category.id = len(self.db) + 1
        self.db.append(category.__dict__)

    def get(self, _id: int) -> Category:
        for el in self.db:
            if el['id'] == _id:
                return Category(**el)
        raise DataNotFoundException

    def get_all(self) -> list[Category]:
        return [Category(**data) for data in self.db]

    def delete(self, _id: int) -> None:
        pass

    def update(self, _id: int, category: Category) -> None:
        pass
