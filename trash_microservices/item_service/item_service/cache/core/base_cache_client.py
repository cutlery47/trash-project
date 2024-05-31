from abc import ABC, abstractmethod
from pydantic import BaseModel

from typing import Optional

class BaseCacheClient(ABC):

    @abstractmethod
    async def get(self, name: str, id_: int) -> dict | None:
        """
        returns data, stored in cache, if any
        :param name:
        :param id_:
        :return:
        """
        raise NotImplementedError

    @abstractmethod
    async def set(self, name: str,  data: dict, id_: int) -> None:
        """
        updates data stored in cache by a key, if any
        :param id_:
        :param name:
        :param data:
        :return:
        """
        raise NotImplementedError

    @abstractmethod
    async def delete(self, name: str, id_: int) -> None:
        """
        deletes data stored in cache by a key, if any
        :param name:
        :param id_:
        :return:
        """
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    async def _generate_key(name: str, id_: int) -> str:
        """
        generate a key for cache storage
        :param: name
        :param id_:
        :return:
        """
        raise NotImplementedError
