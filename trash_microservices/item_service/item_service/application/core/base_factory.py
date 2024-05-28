from abc import ABC, abstractmethod

from item_service.application.core.base_application import BaseApplication

from item_service.config.app.app_config import AppConfig
from item_service.config.database.db_config import DBConfig


class BaseFactory(ABC):

    @staticmethod
    @abstractmethod
    def setup_loggers() -> None:
        """
        Here you would set up your logger handlers
        :return: None
        """
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def parse_configs(app_config_path: str,
                      db_config_path: str,
                      cache_config_path: str,
                      urls_path: str) -> tuple[AppConfig, DBConfig, dict]:
        """
        Handles JSON configs and returns config dataclasses
        :return: tuple[AppConfig, DBConfig, dict]
        """
        raise NotImplementedError

    @abstractmethod
    def create(self) -> BaseApplication:
        """
        Returns application instance
        :return: BaseApplication
        """
        raise NotImplementedError
