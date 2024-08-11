from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, AsyncSession

class BaseRepository[Entity](ABC):

    @abstractmethod
    async def create(self, entity: Entity) -> Entity:
        """
        Creates a new entity in the repositories.
        :param entity:
        :return:
        """
        raise NotImplementedError

    @abstractmethod
    async def get(self, *filters) -> list[Entity]:
        """
        Retrieves an entity from the repositories.
        :param entity_id:
        :return:
        """
        raise NotImplementedError

    @abstractmethod
    async def update(self, entity: Entity, *filters) -> Entity:
        """
        Updates an entity in the repositories.
        :param entity_id:
        :param entity:
        :return:
        """
        raise NotImplementedError

    @abstractmethod
    async def delete(self, *filters) -> None:
        """
        Deletes an entity from the repositories.
        :param entity_id:
        :return:
        """
        raise NotImplementedError
