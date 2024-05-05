from item_service.interfaces.base_service import BaseService
from item_service.schemas.item_schema import BaseItem, Item, ItemAdd
from item_service.repositories.models.models import Item
from item_service.repositories.item_repository import ItemRepository

class ItemService(BaseService[BaseItem]):
    def __init__(self, repository: ItemRepository):
        self.repository = repository

    async def create(self, item: ItemAdd) -> None:

        await self.repository.create(item)

    async def get(self, item_id: int) -> Item:
        # return await self.repository.get(item_id)
        return await self.repository.get(item_id)

    async def get_all(self) -> list[Item]:
        return await self.repository.get_all()

    async def update(self, item_id: int, item: ItemAdd) -> None:
        pass

    async def delete(self, item_id: int) -> None:
        pass
