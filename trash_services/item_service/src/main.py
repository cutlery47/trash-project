from src.application.application import Application
from src.application.factory import ApplicationFactory

from src.controller.controller import Controller
from src.controller.handlers.validator import RequestValidator

from src.services.services.review_service import ReviewService
from src.services.services.item_service import ItemService
from src.services.services.category_service import CategoryService

from src.repositories.repositories.repositories import ItemRepository, CategoryRepository, ReviewRepository
from src.repositories.handlers.exception_handler import RepositoryExceptionHandler

from src.cache.redis_client_factory import RedisClientFactory

from redis.asyncio.connection import ConnectionPool

factory = ApplicationFactory(application_class=Application,
                             controller_class=Controller,

                             item_service_class=ItemService,
                             review_service_class=ReviewService,
                             category_service_class=CategoryService,

                             request_validator_class=RequestValidator,

                             item_repository_class=ItemRepository,
                             review_repository_class=ReviewRepository,
                             category_repository_class=CategoryRepository,

                             repository_exc_handler_class=RepositoryExceptionHandler,

                             db_config_path="src/config/database/db_config.json",
                             app_config_path="src/config/app/app_config.json",
                             urls_path="src/config/app/urls.json")
# === Entrypoint ===
app = factory.create().asgi_app()
