from fastapi import FastAPI

from item_service.interfaces.base_application import BaseApplication
from item_service.interfaces.base_controller import BaseController

from item_service.services.item_service import ItemService
from item_service.services.review_service import ReviewService
from item_service.services.category_service import CategoryService

from item_service.repositories.item_repository import ItemRepository
from item_service.repositories.review_repository import ReviewRepository
from item_service.repositories.category_repository import CategoryRepository

from item_service.config.app_config import AppConfig
from item_service.config.db_config import DBConfig

from sqlalchemy.engine import create_engine

from loguru import logger

import json
import sys

class ApplicationFactory:
    def __init__(self,
                 application: type(BaseApplication),
                 controller: type(BaseController),

                 item_service: type(ItemService),
                 review_service: type(ReviewService),
                 category_service: type(CategoryService),

                 item_repository: type(ItemRepository),
                 review_repository: type(ReviewRepository),
                 category_repository: type(CategoryRepository),

                 app_config_path: str,
                 db_config_path: str,
                 urls_path: str,
                 ):
        self.setup_loggers()
        app_config, db_config, urls = self.parse_configs(app_config_path, db_config_path, urls_path)
        alchemy_engine = create_engine(f"{db_config.driver}"
                                       f"://{db_config.username}:"
                                       f"{db_config.password}@"
                                       f"{db_config.host}:"
                                       f"{db_config.port}/"
                                       f"{db_config.dbname}")

        item_service = item_service(item_repository(alchemy_engine))
        review_service = review_service(review_repository(alchemy_engine))
        category_service = category_service(category_repository(alchemy_engine))

        controller = controller(item_service, review_service, category_service, urls)
        self.app = application(controller, app_config)

    @staticmethod
    def setup_loggers():
        # file logger
        logger.add(sink="logs/logs.json",
                   level="ERROR",
                   format="{time:DD/MM/YYYY/HH:mm:ss} "
                          "|{level}| line {line} in {module}.{function}: {message}",
                   colorize=True,
                   serialize=True,
                   rotation="1 MB",
                   compression="zip")

    @staticmethod
    def parse_configs(app_config_path: str, db_config_path: str, urls_path:str) -> tuple[AppConfig, DBConfig, dict]:
        app_config_dict = json.load(open(app_config_path))
        db_config_dict = json.load(open(db_config_path))
        urls = json.load(open(urls_path))

        app_config = AppConfig(**app_config_dict)
        db_config = DBConfig(**db_config_dict)

        return app_config, db_config, urls

    def create(self) -> FastAPI:
        return self.app.asgi_app()
