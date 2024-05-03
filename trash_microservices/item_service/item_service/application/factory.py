from fastapi import FastAPI

from item_service.interfaces.base_application import BaseApplication
from item_service.interfaces.base_controller import BaseController
from item_service.interfaces.base_service import BaseService
from item_service.interfaces.base_repository import BaseRepository
from item_service.config.app_config import AppConfig
from item_service.config.db_config import DBConfig

from sqlalchemy.engine import create_engine

import json

class ApplicationFactory:
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
                 ):
        app_config, db_config = self.parse_configs(app_config_path, db_config_path)
        alchemy_engine = create_engine(f"postgresql+psycopg2://cutlery:12345@localhost:5432/item_service")

        item_service = item_service(item_repository(alchemy_engine))
        review_service = review_service(review_repository(alchemy_engine))
        category_service = category_service(category_repository(alchemy_engine))

        controller = controller(item_service, review_service, category_service)
        self.app = application(controller, app_config)

    @staticmethod
    def parse_configs(app_config_path: str, db_config_path: str) -> tuple[AppConfig, DBConfig]:
        app_config_dict = json.load(open(app_config_path))
        db_config_dict = json.load(open(db_config_path))

        app_config = AppConfig(**app_config_dict)
        db_config = DBConfig(**db_config_dict)

        return app_config, db_config

    def create(self) -> FastAPI:
        return self.app.asgi_app()
