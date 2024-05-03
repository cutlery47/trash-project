from abc import ABC, abstractmethod

from sqlalchemy.engine import Engine

class RepositoryInterface[Entity](ABC):
    @abstractmethod
    def __init__(self, engine: Engine) -> None:
        raise NotImplementedError

    @abstractmethod
    async def create(self, entity: Entity) -> None:
        """
        Creates a new entity in the repositories.
        :param entity:
        :return:
        """
        raise NotImplementedError

    @abstractmethod
    async def get(self, entity_id: Entity) -> Entity:
        """
        Retrieves an entity from the repositories.
        :param entity_id:
        :return:
        """
        raise NotImplementedError

    @abstractmethod
    async def get_all(self) -> list[Entity]:
        """
        Retrieves all entities from the repositories.
        :return:
        """
        raise NotImplementedError

    @abstractmethod
    async def update(self, entity_id: int, entity: Entity) -> None:
        """
        Updates an entity in the repositories.
        :param entity_id:
        :param entity:
        :return:
        """
        raise NotImplementedError

    @abstractmethod
    async def delete(self, entity_id: int) -> None:
        """
        Deletes an entity from the repositories.
        :param entity_id:
        :return:
        """
        raise NotImplementedError
