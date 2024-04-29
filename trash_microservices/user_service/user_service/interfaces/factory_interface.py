from abc import ABC, abstractmethod


class FactoryInterface(ABC):
    @classmethod
    @abstractmethod
    def create(cls,
               app_config,
               db_config,
               jwt_secret_path):
        raise NotImplementedError
