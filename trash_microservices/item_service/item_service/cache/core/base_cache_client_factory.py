from abc import ABC, abstractmethod

from item_service.cache.core.base_cache_client import BaseCacheClient

class BaseCacheClientFactory(ABC):
    @abstractmethod
    def __init__(self):
        raise NotImplementedError

    @abstractmethod
    def create(self) -> BaseCacheClient:
        """
        returns a cache client
        :return:
        """
        raise NotImplementedError