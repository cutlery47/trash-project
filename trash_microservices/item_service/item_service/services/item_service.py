from item_service.interfaces.base_service import BaseService
from item_service.interfaces.base_repository import BaseRepository
from item_service.schemas.item_schema import BaseItem, Item, ItemAdd


class ItemService(BaseService[BaseItem]):
    def __init__(self, repository: BaseRepository):
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
