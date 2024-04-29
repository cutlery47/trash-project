from django.core.wsgi import get_wsgi_application
from django.urls import path, include

from item_service.controller.controller import Controller
from item_service.repository.repository import Repository
from item_service.router.router import Router
from item_service.service.service import Service

class Application:
    def __init__(self, router):
        self.router = router

    def urls(self):
        return self.router.urls

    @staticmethod
    def wsgi():
        return get_wsgi_application()

class ApplicationFactory:
    def __init__(self,
                 repository: type(Repository),
                 controller: type(Controller),
                 service: type(Service),
                 router: type(Router)
                 ):
        repository = repository()
        service = service(repository)
        controller = controller(service)
        router = router(controller)

        self.application = Application(router)

    def create(self):
        return self.application


app = ApplicationFactory(Repository, Controller, Service, Router).create()
urlpatterns = app.router.routes
wsgi_app = app.wsgi()
