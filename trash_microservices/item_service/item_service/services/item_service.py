from item_service.interfaces.service import ServiceInterface
from item_service.interfaces.repository import RepositoryInterface
from item_service.schemas.item_schema import BaseItem, Item, ItemAdd


class ItemService(ServiceInterface[BaseItem]):
    def __init__(self, repository: RepositoryInterface):
        self.repository = repository

    async def create(self, item: ItemAdd) -> None:
        # return await self.repository.create(item)
        pass

    async def get(self, item_id: int) -> Item:
        # return await self.repository.get(item_id)
        pass

    async def get_all(self) -> list[Item]:
        return await self.repository.get_all()

    async def update(self, item_id: int, item: ItemAdd) -> None:
        pass

    async def delete(self, item_id: int) -> None:
        pass
