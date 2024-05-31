from abc import ABC, abstractmethod
from pydantic import BaseModel

from typing import Optional

class BaseCacheClient(ABC):

    @abstractmethod
    async def get(self, entity_class: str, entity_id: int) -> BaseModel | None:
        """
        returns data, stored in cache, if any
        :param entity_class:
        :param entity_id:
        :return:
        """
        raise NotImplementedError

    @abstractmethod
    async def set(self, entity_class: str, entity: BaseModel) -> None:
        """
        updates data stored in cache by a key, if any
        :param entity:
        :param entity_class:
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
