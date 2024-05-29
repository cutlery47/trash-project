from item_service.services.core.base_service import BaseService
from item_service.repositories.core.base_repository import BaseRepository
from item_service.cache.core.base_cache_client_factory import BaseCacheClientFactory

from pydantic import BaseModel

from item_service.models.models import Base

from loguru import logger

from typing import Optional

# maybe shouldve used filters instead of explicit arguments

class CRUDService[AddDTO, DTO](BaseService):
    _dto_class = BaseModel
    _add_dto_class = BaseModel
    _entity_class = Base

    def __init__(self, repository: BaseRepository, cache_client_factory: Optional[BaseCacheClientFactory] = None):
        self._repository = repository
        self._cache_client_factory = cache_client_factory

    async def create(self, dto: AddDTO) -> None:
        cache_client = self._cache_client_factory.create()
        entity = self._entity_class(**dto.model_dump())
        await self._repository.create(entity)

    async def get(self, dto_id: Optional[int] = None) -> list[DTO]:
        if dto_id is not None:
            orm_data = await self._repository.get(self._entity_class.id == dto_id)
        else:
            orm_data = await self._repository.get()

        return [self._dto_class.model_validate(data, from_attributes=True) for data in orm_data]

    async def update(self, dto_id: int, dto: AddDTO) -> None:
        entity = self._entity_class(**dto.model_dump())
        await self._repository.update(entity, self._entity_class.id == dto_id)

    async def delete(self, dto_id: int) -> None:
        await self._repository.delete(self._entity_class.id == dto_id)



