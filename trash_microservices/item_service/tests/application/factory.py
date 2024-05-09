from item_service.interfaces.base_factory import BaseFactory
from item_service.interfaces.base_application import BaseApplication
from item_service.interfaces.base_controller import BaseController
from item_service.interfaces.base_service import BaseService
from item_service.interfaces.base_repository import BaseRepository

from item_service.config.app_config import AppConfig
from item_service.config.db_config import DBConfig

from loguru import logger

import json

class TestApplicationFactory(BaseFactory):
    def __init__(self,
                 application: type(BaseApplication),
                 controller: type(BaseController),

                 item_service: type(BaseService),
                 review_service: type(BaseService),
                 category_service: type(BaseService),

                 item_repository: type(BaseRepository),
                 review_repository: type(BaseRepository),
                 category_repository: type(BaseRepository),

                 app_config_path: str,
                 db_config_path: str,
                 urls_path: str
                 ):
        self.setup_loggers()
        app_config, db_config, urls = self.parse_configs(app_config_path, db_config_path, urls_path)

        item_service = item_service(item_repository())
        review_service = review_service(review_repository())
        category_service = category_service(category_repository())

        controller = controller(item_service, review_service, category_service, urls)
        self.application = application(controller, app_config)

    @staticmethod
    def setup_loggers() -> None:
        logger.add(sink="logs/logs.json",
                   level="ERROR",
                   format="{time:DD/MM/YYYY/HH:mm:ss} "
                          "|{level}| line {line} in {module}.{function}: {message}",
                   colorize=True,
                   serialize=True,
                   rotation="1 MB",
                   compression="zip")

    @staticmethod
    def parse_configs(app_config_path: str, db_config_path: str, urls_path: str) -> tuple[AppConfig, DBConfig, dict]:
        app_config_dict = json.load(open(app_config_path))
        db_config_dict = json.load(open(db_config_path))
        urls = json.load(open(urls_path))

        app_config = AppConfig(**app_config_dict)
        db_config = DBConfig(**db_config_dict)

        return app_config, db_config, urls

    def create(self) -> BaseApplication:
        return self.application