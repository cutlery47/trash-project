from abc import ABC, abstractmethod

from item_service.controller.validator import RequestValidator
from item_service.interfaces.base_application import BaseApplication
from item_service.interfaces.base_controller import BaseController
from item_service.interfaces.base_service import BaseService
from item_service.interfaces.base_repository import BaseRepository

from item_service.config.app_config import AppConfig
from item_service.config.db_config import DBConfig


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
    def parse_configs(app_config_path: str, db_config_path: str, urls_path: str) -> tuple[AppConfig, DBConfig, dict]:
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
