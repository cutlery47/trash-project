from fastapi import FastAPI

from item_service.interfaces.application import ApplicationInterface
from item_service.interfaces.controller import ControllerInterface
from item_service.interfaces.service import ServiceInterface
from item_service.interfaces.repository import RepositoryInterface

class ApplicationFactory:
    def __init__(self,
                 application: type(ApplicationInterface),
                 controller: type(ControllerInterface),
                 service: type(ServiceInterface),
                 repository: type(RepositoryInterface),
                 app_config: dict
                 ):
        repository = repository()
        service = service(repository)
        controller = controller(service)

        self.app = application(controller, app_config)

    def create(self) -> FastAPI:
        return self.app.asgi_app()
