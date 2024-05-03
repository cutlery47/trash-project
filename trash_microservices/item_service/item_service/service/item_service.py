from item_service.interfaces.service import ServiceInterface
from item_service.interfaces.repository import RepositoryInterface
from item_service.schemas.item_schema import BaseItem, Item, ItemAdd


class ItemService(ServiceInterface[BaseItem]):
    def __init__(self, repository: RepositoryInterface):
        self.repository = repository

    async def create(self, item: ItemAdd) -> None:
        pass

    async def get(self, item_id: int) -> Item:
        pass

    async def get_all(self) -> list[Item]:
        pass

    async def update(self, item_id: int, item: ItemAdd) -> None:
        pass

    async def delete(self, item_id: int) -> None:
        pass
