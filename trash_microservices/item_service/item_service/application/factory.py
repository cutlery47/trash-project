from item_service.application.core.base_application import BaseApplication
from item_service.application.core.base_factory import BaseFactory

from item_service.controller.core.base_controller import BaseController
from item_service.controller.handlers.validator import RequestValidator

from item_service.services.core.base_service import BaseService
from item_service.cache.core.base_cache_client import BaseCacheManager

from item_service.repositories.core.base_repository import BaseRepository
from item_service.repositories.core.base_exception_handler import BaseExceptionHandler

from item_service.config.app.app_config import AppConfig
from item_service.config.database.db_config import DBConfig
from item_service.config.cache.cache_config import CacheConfig

from aioredis import ConnectionPool

from typing import Optional

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from loguru import logger

import json

# TODO: create a logger for successful operations only

class ApplicationFactory(BaseFactory):
    def __init__(self,
                 application: type(BaseApplication),

                 controller: type(BaseController),
                 request_validator: type(RequestValidator),

                 item_service: type(BaseService),
                 review_service: type(BaseService),
                 category_service: type(BaseService),

                 item_repository: type(BaseRepository),
                 review_repository: type(BaseRepository),
                 category_repository: type(BaseRepository),
                 repository_exc_handler: type(BaseExceptionHandler),

                 app_config_path: str,
                 db_config_path: str,
                 urls_path: str,

                 cache_config_path: Optional[str] = None
                 cache_client_factory:
                 ):

        self.setup_loggers()

        urls, app_config, db_config, cache_config = self.parse_configs(urls_path=urls_path,
                                                                       app_config_path=app_config_path,
                                                                       db_config_path=db_config_path,
                                                                       cache_config_path=cache_config_path)

        alchemy_engine = create_async_engine(f"{db_config.driver}"f"://{db_config.username}:"
                                             f"{db_config.password}@"f"{db_config.host}:"
                                             f"{db_config.port}/"f"{db_config.dbname}")

        sessionmaker = async_sessionmaker(bind=alchemy_engine, expire_on_commit=False)

        # passing the single instance of handler to each repo
        # may cause some drawbacks which I can't think of currently
        repository_exc_handler = repository_exc_handler()

        item_repository = item_repository(engine=alchemy_engine,
                                          sessionmaker=sessionmaker,
                                          exc_handler=repository_exc_handler)

        review_repository = review_repository(engine=alchemy_engine,
                                              sessionmaker=sessionmaker,
                                              exc_handler=repository_exc_handler)

        category_repository = category_repository(engine=alchemy_engine,
                                                  sessionmaker=sessionmaker,
                                                  exc_handler=repository_exc_handler)

        if cache_config:


        item_service = item_service(repository=item_repository, cache_manager=cache_manager)
        review_service = review_service(repository=review_repository, cache_manager=cache_manager)
        category_service = category_service(repository=category_repository, cache_manager=cache_manager)

        request_validator = request_validator(urls=urls)
        controller = controller(item_service=item_service,
                                review_service=review_service,
                                category_service=category_service,
                                request_validator=request_validator)

        self.app = application(controller, app_config)

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

    @staticmethod
    def parse_configs(app_config_path: str,
                      db_config_path: str,
                      urls_path: str,
                      cache_config_path: Optional[str] = None,
                      ) -> tuple[dict, AppConfig, DBConfig, CacheConfig | None]:
        urls = json.load(open(urls_path))

        app_config_dict = json.load(open(app_config_path))
        app_config = AppConfig(**app_config_dict)

        db_config_dict = json.load(open(db_config_path))
        db_config = DBConfig(**db_config_dict)

        cache_config = None
        if cache_config_path:
            cache_config_dict = json.load(open(cache_config_path))
            cache_config = CacheConfig(**cache_config_dict)

        return urls, app_config, db_config, cache_config

    def create(self) -> BaseApplication:
        return self.app
