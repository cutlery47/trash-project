from abc import ABC, abstractmethod

class BaseCacheClientFactory[Client](ABC):
    @abstractmethod
    def create(self) -> Client:
        """
        returns a cache client
        :return:
        """
        raise NotImplementedError