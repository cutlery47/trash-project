from abc import ABC, abstractmethod, abstractproperty

class BaseExceptionHandler(ABC):

    @classmethod
    @abstractmethod
    def handle(cls, exc: Exception):
        """
        handles provided error
        :param exc:
        :return:
        """
        raise NotImplementedError