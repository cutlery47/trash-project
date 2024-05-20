from item_service.interfaces.base_application import BaseApplication
from item_service.interfaces.base_factory import BaseFactory

from typing import Annotated

from fastapi import Depends

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from loguru import logger

import json

# TODO: create a logger for successful operations only

class ApplicationFactory(BaseFactory):
    def __init__(self,
                 application: Annotated[BaseApplication, Depends(get_application)],
                 ):

        self.setup_loggers()
        self.app = application

        # alchemy_engine = create_async_engine(f"{db_config.driver}"f"://{db_config.username}:"
        #                                      f"{db_config.password}@"f"{db_config.host}:"
        #                                      f"{db_config.port}/"f"{db_config.dbname}")
        # sessionmaker = async_sessionmaker(bind=alchemy_engine, expire_on_commit=False)

    @staticmethod
    def setup_loggers():
        # file logger
        logger.add(sink="item_service/logs/logs.json",
                   level="ERROR",
                   format="{time:DD/MM/YYYY/HH:mm:ss} "
                          "|{level}| line {line} in {module}.{function}: {message}",
                   colorize=True,
                   serialize=True,
                   rotation="1 MB",
                   compression="zip")

    # @staticmethod
    # def parse_configs(app_config_path: str, db_config_path: str, urls_path: str) -> tuple[AppConfig, DBConfig, dict]:
    #     app_config_dict = json.load(open(app_config_path))
    #     db_config_dict = json.load(open(db_config_path))
    #     urls = json.load(open(urls_path))
    #
    #     app_config = AppConfig(**app_config_dict)
    #     db_config = DBConfig(**db_config_dict)
    #
    #     return app_config, db_config, urls

    def create(self) -> BaseApplication:
        return self.app
