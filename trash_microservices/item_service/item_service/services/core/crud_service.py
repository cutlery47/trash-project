from item_service.services.core.base_service import BaseService
from item_service.repositories.core.base_repository import BaseRepository
from item_service.cache.core.base_cache_manager import BaseCacheManager

from pydantic import BaseModel

from item_service.models.models import Base

from loguru import logger

from typing import Optional

# maybe shouldve used filters instead of explicit arguments

class CRUDService[AddDTO, DTO](BaseService):
    _dto_class = BaseModel
    _add_dto_class = BaseModel
    _entity_class = Base

    def __init__(self, repository: BaseRepository, cache_manager: Optional[BaseCacheManager] = None):
        self.repository = repository
        self.cache_manager = cache_manager

    async def create(self, dto: AddDTO) -> None:
        entity = self._entity_class(**dto.model_dump())
        await self.repository.create(entity)

    async def get(self, dto_id: Optional[int] = None) -> list[DTO]:
        # orm_data = self.cache_manager.get(type(self._entity_class).__name__, dto_id)
        # if not orm_data:
        if dto_id is not None:
            orm_data = await self.repository.get(self._entity_class.id == dto_id)
        else:
            orm_data = await self.repository.get()

        return [self._dto_class.model_validate(data, from_attributes=True) for data in orm_data]

    async def update(self, dto_id: int, dto: AddDTO) -> None:
        entity = self._entity_class(**dto.model_dump())
        await self.repository.update(entity, self._entity_class.id == dto_id)

    async def delete(self, dto_id: int) -> None:
        await self.repository.delete(self._entity_class.id == dto_id)



