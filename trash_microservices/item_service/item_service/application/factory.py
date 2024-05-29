from item_service.application.core.base_application import BaseApplication
from item_service.application.core.base_factory import BaseFactory

from item_service.controller.core.base_controller import BaseController
from item_service.controller.handlers.validator import RequestValidator

from item_service.services.core.base_service import BaseService

from item_service.repositories.core.base_repository import BaseRepository
from item_service.repositories.core.base_exception_handler import BaseExceptionHandler

from item_service.config.app.app_config import AppConfig
from item_service.config.database.db_config import DBConfig
from item_service.config.cache.cache_config import CacheConfig

from item_service.cache.core.base_cache_client_factory import BaseCacheClientFactory

from typing import Optional, Any

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from loguru import logger

from dataclasses import asdict

from redis.asyncio.connection import ConnectionPool

import json


# TODO: create a logger for successful operations only
# TODO: figure out how to enable type hints here

class ApplicationFactory(BaseFactory):
    def __init__(self,
                 application_class: type(BaseApplication),

                 controller_class: type(BaseController),
                 request_validator_class: type(RequestValidator),

                 item_service_class: type(BaseService),
                 review_service_class: type(BaseService),
                 category_service_class: type(BaseService),

                 item_repository_class: type(BaseRepository),
                 review_repository_class: type(BaseRepository),
                 category_repository_class: type(BaseRepository),
                 repository_exc_handler_class: type(BaseExceptionHandler),

                 app_config_path: str,
                 db_config_path: str,
                 urls_path: str,

                 cache_config_path: Optional[str] = None,
                 cache_client_factory_class: Optional[type(BaseCacheClientFactory)] = None,
                 cache_connection_pool_class: Optional[type(ConnectionPool) | Any] = None
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
        repository_exc_handler = repository_exc_handler_class()

        item_repository = item_repository_class(engine=alchemy_engine,
                                                sessionmaker=sessionmaker,
                                                exc_handler=repository_exc_handler)

        review_repository = review_repository_class(engine=alchemy_engine,
                                                    sessionmaker=sessionmaker,
                                                    exc_handler=repository_exc_handler)

        category_repository = category_repository_class(engine=alchemy_engine,
                                                        sessionmaker=sessionmaker,
                                                        exc_handler=repository_exc_handler)

        cache_client_factory = None
        if cache_config and cache_connection_pool_class and cache_client_factory_class:
            cache_connection_pool = cache_connection_pool_class(**asdict(cache_config))
            cache_client_factory = cache_client_factory_class(connection_pool=cache_connection_pool)

        item_service = item_service_class(repository=item_repository,
                                          cache_client_factory=cache_client_factory)

        review_service = review_service_class(repository=review_repository,
                                              cache_client_factory=cache_client_factory)

        category_service = category_service_class(repository=category_repository,
                                                  cache_client_factory=cache_client_factory)

        request_validator = request_validator_class(urls=urls)

        controller = controller_class(item_service=item_service,
                                      review_service=review_service,
                                      category_service=category_service,
                                      request_validator=request_validator)

        self.app = application_class(controller, app_config)

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
