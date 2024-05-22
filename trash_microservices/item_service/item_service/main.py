from item_service.application.application import Application
from item_service.controller.controller import Controller
from item_service.services.core.crud_service import CRUDService
from item_service.repositories.core.crud_repository import CRUDRepository
from item_service.controller.validator import RequestValidator
from item_service.repositories.handlers.exception_handler import RepositoryExceptionHandler
from item_service.repositories.models.models import Item, Category, Review
from item_service.application.factory import ApplicationFactory

from item_service.schemas.schemas.category_schema import CategoryDTO, CategoryAddDTO
from item_service.schemas.schemas.item_schema import ItemDTO, ItemAddDTO
from item_service.schemas.schemas.review_schema import ReviewDTO, ReviewAddDTO

factory = ApplicationFactory(application=Application,
                             controller=Controller,

                             item_service=CRUDService[ItemAddDTO, ItemDTO],
                             review_service=CRUDService[ReviewAddDTO, ReviewDTO],
                             category_service=CRUDService[CategoryAddDTO, CategoryDTO],

                             request_validator=RequestValidator,

                             item_repository=CRUDRepository[Item],
                             review_repository=CRUDRepository[Review],
                             category_repository=CRUDRepository[Category],

                             repository_exc_handler=RepositoryExceptionHandler,

                             db_config_path="item_service/config/db_config.json",
                             app_config_path="item_service/config/app_config.json",
                             urls_path="item_service/config/urls.json"
                             )
# === Entrypoint ===
app = factory.create().asgi_app()
