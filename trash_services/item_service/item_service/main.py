from item_service.application.application import Application
from item_service.application.factory import ApplicationFactory

from item_service.controller.controller import Controller
from item_service.controller.handlers.validator import RequestValidator

from item_service.services.services.review_service import ReviewService
from item_service.services.services.item_service import ItemService
from item_service.services.services.category_service import CategoryService

from item_service.repositories.repositories.repositories import ItemRepository, CategoryRepository, ReviewRepository
from item_service.repositories.handlers.exception_handler import RepositoryExceptionHandler

from item_service.cache.redis_client_factory import RedisClientFactory

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

                             db_config_path="item_service/config/database/db_config.json",
                             app_config_path="item_service/config/app/app_config.json",
                             urls_path="item_service/config/app/urls.json",

                             cache_client_factory_class=RedisClientFactory,
                             cache_connection_pool_class=ConnectionPool,
                             cache_config_path="item_service/config/cache/cache_config.json")
# === Entrypoint ===
app = factory.create().asgi_app()
