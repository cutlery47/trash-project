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
                 application_class: BaseApplication.__class__,

                 controller_class: BaseController.__class__,
                 request_validator_class: RequestValidator.__class__,

                 item_service_class: BaseService.__class__,
                 review_service_class: BaseService.__class__,
                 category_service_class: BaseService.__class__,

                 item_repository_class: BaseRepository.__class__,
                 review_repository_class: BaseRepository.__class__,
                 category_repository_class: BaseRepository.__class__,
                 repository_exc_handler_class: BaseExceptionHandler.__class__,

                 app_config_path: str,
                 db_config_path: str,
                 urls_path: str,

                 cache_config_path: str = None,
                 cache_client_factory_class: BaseCacheClientFactory.__class__ = None,
                 cache_connection_pool_class: ConnectionPool.__class__ | Any = None
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
        repository_exc_handler: BaseExceptionHandler = repository_exc_handler_class()

        item_repository: BaseRepository = item_repository_class(engine=alchemy_engine,
                                                                sessionmaker=sessionmaker,
                                                                exc_handler=repository_exc_handler)

        review_repository: BaseRepository = review_repository_class(engine=alchemy_engine,
                                                                    sessionmaker=sessionmaker,
                                                                    exc_handler=repository_exc_handler)

        category_repository: BaseRepository = category_repository_class(engine=alchemy_engine,
                                                                        sessionmaker=sessionmaker,
                                                                        exc_handler=repository_exc_handler)

        cache_client_factory = None
        if cache_config and cache_connection_pool_class and cache_client_factory_class:
            cache_connection_pool = cache_connection_pool_class(**asdict(cache_config))
            cache_client_factory = cache_client_factory_class(connection_pool=cache_connection_pool)

        item_service: BaseService = item_service_class(repository=item_repository,
                                                       cache_client_factory=cache_client_factory)

        review_service: BaseService = review_service_class(repository=review_repository,
                                                           cache_client_factory=cache_client_factory)

        category_service: BaseService = category_service_class(repository=category_repository,
                                                               cache_client_factory=cache_client_factory)

        request_validator: RequestValidator = request_validator_class(urls=urls)

        controller: BaseController = controller_class(item_service=item_service,
                                                      review_service=review_service,
                                                      category_service=category_service,
                                                      request_validator=request_validator)

        self.app: BaseApplication = application_class(controller, app_config)

    @staticmethod
    def setup_loggers():
        logger.remove()

        # file logger
        logger.add(sink="item_service/logs/err_logs.json",
                   level="ERROR",
                   format="{time:DD/MM/YYYY/HH:mm:ss} "
                          "|{level}| line {line} in {module}.{function}: {message}",
                   colorize=True,
                   serialize=True,
                   rotation="1 MB",
                   compression="zip")

        logger.add(sink="item_service/logs/logs.json",
                   level="INFO",
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
