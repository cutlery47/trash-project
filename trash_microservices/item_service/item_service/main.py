from item_service.application.application import Application
from item_service.router.router import Router
from item_service.controller.controller import Controller
from item_service.service.service import Service
from item_service.repository.repository import Repository

from item_service.application.factory import ApplicationFactory

factory = ApplicationFactory(application=Application,
                             router=Router,
                             controller=Controller,
                             service=Service,
                             repository=Repository,
                             app_config={})
# === Entrypoint ===
app = factory.create()
