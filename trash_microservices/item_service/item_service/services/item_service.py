from item_service.interfaces.base_service import BaseService
from item_service.schemas.item_schema import BaseItemDTO, ItemDTO, ItemAddDTO
from item_service.repositories.models.models import Item
from item_service.interfaces.base_repository import BaseRepository

from loguru import logger

class ItemService(BaseService[BaseItemDTO]):
    def __init__(self, repository: BaseRepository):
        self.repository = repository

    async def create(self, item: ItemAddDTO) -> None:
        orm_item = Item(**item.model_dump())
        await self.repository.create(orm_item)

    async def get(self, item_id: int) -> ItemDTO:
        orm_item = await self.repository.get(item_id)
        return ItemDTO.model_validate(orm_item, from_attributes=True)

    async def get_all(self) -> list[ItemDTO]:
        orm_items = await self.repository.get_all()
        return [ItemDTO.model_validate(orm_item, from_attributes=True) for orm_item in orm_items]

    async def delete(self, item_id: int) -> None:
        await self.repository.delete(item_id)

    async def update(self, item_id: int, item: ItemAddDTO) -> None:
        orm_item = Item(**item.model_dump())
        await self.repository.update(item_id, orm_item)
