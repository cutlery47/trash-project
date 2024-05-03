from fastapi import FastAPI

from item_service.interfaces.application import ApplicationInterface
from item_service.interfaces.controller import ControllerInterface
from item_service.interfaces.service import ServiceInterface
from item_service.interfaces.repository import RepositoryInterface

from sqlalchemy.engine import create_engine

class ApplicationFactory:
    def __init__(self,
                 application: type(ApplicationInterface),
                 controller: type(ControllerInterface),

                 item_service: type(ServiceInterface),
                 review_service: type(ServiceInterface),
                 category_service: type(ServiceInterface),

                 item_repository: type(RepositoryInterface),
                 review_repository: type(RepositoryInterface),
                 category_repository: type(RepositoryInterface),

                 app_config: dict,
                 db_config: dict,
                 ):
        alchemy_engine = create_engine("postgresql+psycopg2://cutlery:12345@localhost:5432/item_service")

        item_service = item_service(item_repository(alchemy_engine))
        review_service = review_service(review_repository(alchemy_engine))
        category_service = category_service(category_repository(alchemy_engine))

        controller = controller(item_service, review_service, category_service)
        self.app = application(controller, app_config)

    def create(self) -> FastAPI:
        return self.app.asgi_app()
