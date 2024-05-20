from item_service.application.application import Application
from item_service.controller.controller import Controller
from item_service.services.item_service import ItemService
from item_service.services.review_service import ReviewService
from item_service.services.category_service import CategoryService
from item_service.repositories.crud_repository import CRUDRepository
from item_service.controller.validator import RequestValidator
from item_service.repositories.handlers.exception_handler import RepositoryExceptionHandler

from fastapi import Depends

from item_service.repositories.models.models import Item, Category, Review

from item_service.application.factory import ApplicationFactory

factory = ApplicationFactory(application=Application,
                             controller=Controller,

                             item_service=ItemService,
                             review_service=ReviewService,
                             category_service=CategoryService,

                             request_validator=RequestValidator,

                             item_repository=CRUDRepository[Item],
                             review_repository=CRUDRepository[Review],
                             category_repository=CRUDRepository[Category],

                             exc_handler

                             db_config_path="item_service/config/db_config.json",
                             app_config_path="item_service/config/app_config.json",
                             urls_path="item_service/config/urls.json"
                             )
# === Entrypoint ===
app = factory.create().asgi_app()
