from abc import ABC, abstractmethod

from item_service.interfaces.base_repository import BaseRepository
from item_service.schemas.item_schema import BaseItemDTO
from item_service.schemas.review_schema import BaseReviewDTO
from item_service.schemas.category_schema import BaseCategoryDTO

class BaseService[Entity: (BaseItemDTO, BaseReviewDTO, BaseCategoryDTO)](ABC):
    @abstractmethod
    def __init__(self, repository: BaseRepository):
        raise NotImplementedError

    @abstractmethod
    async def create(self, entity: Entity) -> None:
        """
        Carries out business logic to create a new entity.
        :param entity:
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
