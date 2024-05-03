from abc import ABC, abstractmethod

from item_service.interfaces.repository import RepositoryInterface
from item_service.schemas.item_schema import BaseItem
from item_service.schemas.review_schema import BaseReview
from item_service.schemas.category_schema import BaseCategory

class ServiceInterface[Entity: (BaseItem, BaseReview, BaseCategory)](ABC):
    @abstractmethod
    def __init__(self, repository: RepositoryInterface):
        raise NotImplementedError

    @abstractmethod
    async def create(self, entity_id: int) -> None:
        """
        Carries out business logic to create a new entity.
        :param entity_id:
        :return:
        """
        raise NotImplementedError

    @abstractmethod
    async def get(self, entity_id: int) -> Entity:
        """
        Carries out business logic to get a specific entity.
        :param entity_id:
        :return:
        """
        raise NotImplementedError

    @abstractmethod
    async def get_all(self) -> list[Entity]:
        """
        Carries out business logic to get all entities.
        :return:
        """
        raise NotImplementedError

    @abstractmethod
    async def update(self, entity_id: int, entity: Entity) -> None:
        """
        Carries out business logic to update a specific entity.
        :param entity_id:
        :param entity:
        :return:
        """
        raise NotImplementedError

    @abstractmethod
    async def delete(self, entity_id: int) -> None:
        """
        Carries out business logic to delete a specific entity.
        :param entity_id:
        :return:
        """
        raise NotImplementedError
