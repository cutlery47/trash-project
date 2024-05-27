from abc import ABC, abstractmethod
from item_service.item_service.models.models import Base

class BaseCacheManager(ABC):

    @abstractmethod
    async def get(self, entity_class: str, entity_id: int) -> Base | None:
        """
        returns data, stored in cache, if any
        :param entity_class:
        :param entity_id:
        :return:
        """
        raise NotImplementedError

    @abstractmethod
    async def set(self, entity_class: str, entity_id: int) -> None:
        """
        updates data stored in cache by a key, if any
        :param entity_class:
        :param entity_id:
        :return:
        """
        raise NotImplementedError

    @abstractmethod
    async def delete(self, entity_class: str, entity_id: int) -> None:
        """
        deletes data stored in cache by a key, if any
        :param entity_class:
        :param entity_id:
        :return:
        """
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    async def _generate_key(entity_class: str, entity_id: int) -> str:
        """
        generate a key for cache storage
        :param entity_class:
        :param entity_id:
        :return:
        """
        raise NotImplementedError
