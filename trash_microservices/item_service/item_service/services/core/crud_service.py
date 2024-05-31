from item_service.services.core.base_service import BaseService
from item_service.repositories.core.base_repository import BaseRepository
from item_service.cache.core.base_cache_client_factory import BaseCacheClientFactory

from pydantic import BaseModel

from item_service.models.models import Base

from dataclasses import asdict

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

    async def create(self, add_dto: AddDTO) -> int:
        # converting dto to model and adding a new record to the database
        entity = self._entity_class(**add_dto.model_dump())
        entity_id = await self._repository.create(entity)

        dto = self._dto_class(id=entity_id, **add_dto.model_dump())

        # if new record was successfully added => creating a cache client and caching the data
        cache_client = self._cache_client_factory.create()
        await cache_client.set(name=self._dto_class.__name__, data=dto.model_dump(), id_=dto.id)

        return entity_id

    async def get(self, dto_id: Optional[int] = None) -> list[DTO]:
        if dto_id is not None:
            # trying to get the data from cache
            cache_client = self._cache_client_factory.create()
            cached_data = await cache_client.get(name=self._dto_class.__name__, id_=dto_id)

            # if value is not cached => search in the database
            if not cached_data:
                orm_data = await self._repository.get(self._entity_class.id == dto_id)
            else:
                return [self._dto_class(**cached_data)]
        else:
            # retrieving the data from database
            orm_data = await self._repository.get()

        logger.info(f"Repo data: {orm_data}")
        return [self._dto_class.model_validate(data, from_attributes=True) for data in orm_data]

    async def update(self, dto_id: int, add_dto: AddDTO) -> None:
        # firstly, update the data in the database
        entity = self._entity_class(**add_dto.model_dump())
        await self._repository.update(entity, self._entity_class.id == dto_id)

        dto = self._dto_class(id=dto_id, **add_dto.model_dump())

        # secondly, update the data in the cache
        cache_client = self._cache_client_factory.create()
        await cache_client.set(name=self._dto_class.__name__, data=dto.model_dump(), id_=dto_id)

    async def delete(self, dto_id: int) -> None:
        # firstly, delete from the database
        await self._repository.delete(self._entity_class.id == dto_id)
        logger.info("here")

        # secondly, delete from the cache
        cache_client = self._cache_client_factory.create()
        await cache_client.delete(self._dto_class.__name__, dto_id)



