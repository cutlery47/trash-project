from item_service.application.application import Application
from item_service.application.factory import ApplicationFactory

from item_service.controller.controller import Controller
from item_service.controller.validator import RequestValidator

from item_service.services.services.review_service import ReviewService
from item_service.services.services.item_service import ItemService
from item_service.services.services.category_service import CategoryService

from item_service.repositories.repositories.item_repository import ItemRepository
from item_service.repositories.repositories.review_repository import ReviewRepository
from item_service.repositories.repositories.category_repository import CategoryRepository
from item_service.repositories.handlers.exception_handler import RepositoryExceptionHandler

factory = ApplicationFactory(application=Application,
                             controller=Controller,

                             item_service=ItemService,
                             review_service=ReviewService,
                             category_service=CategoryService,

                             request_validator=RequestValidator,

                             item_repository=ItemRepository,
                             review_repository=ReviewRepository,
                             category_repository=CategoryRepository,

                             repository_exc_handler=RepositoryExceptionHandler,

                             db_config_path="item_service/config/db_config.json",
                             app_config_path="item_service/config/app_config.json",
                             urls_path="item_service/config/urls.json"
                             )
# === Entrypoint ===
app = factory.create().asgi_app()
