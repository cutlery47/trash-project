from item_service.interfaces.base_service import BaseService
from item_service.interfaces.base_repository import BaseRepository

from pydantic import BaseModel

from item_service.repositories.models.models import Base

from loguru import logger

# maybe shouldve used filters instead of explicit arguments

class CRUDService[AddDTO, DTO: BaseModel](BaseService):
    _entity_class = Base

    def __init__(self, repository: BaseRepository):
        self.repository = repository

    async def create(self, dto: AddDTO) -> None:
        entity = self._entity_class(**dto.model_dump())
        await self.repository.create(entity)

    async def get(self, dto_id: int) -> list[DTO]:
        orm_data = await self.repository.get(self._entity_class.id == dto_id)
        return [DTO.model_validate(data, from_attributes=True) for data in orm_data]

    async def update(self, dto_id: int, dto: AddDTO) -> None:
        entity = self._entity_class(**dto.model_dump())
        await self.repository.update(entity, self._entity_class.id == dto_id)

    async def delete(self, dto_id) -> None:
        await self.repository.delete(self._entity_class.id == dto_id)


