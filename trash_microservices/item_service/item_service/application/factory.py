from item_service.interfaces.base_application import BaseApplication
from item_service.interfaces.base_factory import BaseFactory
from item_service.interfaces.base_controller import BaseController
from item_service.interfaces.base_repository import BaseRepository
from item_service.interfaces.base_service import BaseService
from item_service.controller.validator import RequestValidator
from item_service.interfaces.base_exception_handler import BaseExceptionHandler

from item_service.config.app_config import AppConfig
from item_service.config.db_config import DBConfig

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
                 urls_path: str
                 ):

        self.setup_loggers()
        app_config, db_config, urls = self.parse_configs(app_config_path, db_config_path, urls_path)

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

        item_service = item_service(repository=item_repository)
        review_service = review_service(repository=review_repository)
        category_service = category_service(repository=category_repository)

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
    def parse_configs(app_config_path: str, db_config_path: str, urls_path: str) -> tuple[AppConfig, DBConfig, dict]:
        app_config_dict = json.load(open(app_config_path))
        db_config_dict = json.load(open(db_config_path))
        urls = json.load(open(urls_path))

        app_config = AppConfig(**app_config_dict)
        db_config = DBConfig(**db_config_dict)

        return app_config, db_config, urls

    def create(self) -> BaseApplication:
        return self.app
