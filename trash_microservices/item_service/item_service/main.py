from item_service.application.application import Application
from item_service.controller.controller import Controller
from item_service.services.item_service import ItemService
from item_service.services.review_service import ReviewService
from item_service.services.category_service import CategoryService
from item_service.repositories.item_repository import ItemRepository
from item_service.repositories.review_repository import ReviewRepository
from item_service.repositories.category_repository import CategoryRepository

from item_service.application.factory import ApplicationFactory

factory = ApplicationFactory(application=Application,
                             controller=Controller,

                             item_service=ItemService,
                             review_service=ReviewService,
                             category_service=CategoryService,

                             item_repository=ItemRepository,
                             review_repository=ReviewRepository,
                             category_repository=CategoryRepository,

                             db_config_path="item_service/config/db_config.json",
                             app_config_path="item_service/config/app_config.json",
                             urls_path="item_service/config/urls.json"
                             )
# === Entrypoint ===
app = factory.create()
