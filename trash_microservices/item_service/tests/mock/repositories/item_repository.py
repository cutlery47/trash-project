from item_service.interfaces.base_repository import BaseRepository
from item_service.repositories.models.models import Item
from item_service.exceptions.repository_exceptions import DataNotFoundException


class MockItemRepository(BaseRepository[Item]):
    def __init__(self):
        self.db = []

    def create(self, item: Item) -> None:
        item.id = len(self.db) + 1
        self.db.append(item.__dict__)

    def get(self, _id: int) -> Item:
        for el in self.db:
            if el['id'] == _id:
                return Item(**el)
        raise DataNotFoundException

    def get_all(self) -> list[Item]:
        return [Item(**data) for data in self.db]

    def delete(self, _id: int) -> None:
        pass

    def update(self, _id: int, item: Item) -> None:
        pass