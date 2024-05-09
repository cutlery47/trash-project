from item_service.application.application import Application
from item_service.controller.controller import Controller

from item_service.services.item_service import ItemService
from item_service.services.review_service import ReviewService
from item_service.services.category_service import CategoryService

from tests.application.factory import TestApplicationFactory
from tests.mock.repositories.item_repository import MockItemRepository
from tests.mock.repositories.review_repository import MockReviewRepository
from tests.mock.repositories.category_repository import MockCategoryRepository

factory = TestApplicationFactory(
    application=Application,
    controller=Controller,

    item_service=ItemService,
    review_service=ReviewService,
    category_service=CategoryService,

    item_repository=MockItemRepository,
    review_repository=MockReviewRepository,
    category_repository=MockCategoryRepository,

    app_config_path="config/app_config.json",
    db_config_path="config/db_config.json",
    urls_path="config/urls.json",
)

app = factory.create()
