import pytest

from item_service.application.factory import ApplicationFactory
from item_service.application.application import Application
from item_service.controller.controller import Controller

from item_service.services.item_service import ItemService
from item_service.services.review_service import ReviewService
from item_service.services.category_service import CategoryService

from item_service.repositories.item_repository import ItemRepository
from item_service.repositories.review_repository import ReviewRepository
from item_service.repositories.category_repository import CategoryRepository

from alembic.config import Config

@pytest.fixture(scope="module")
def client():
    app = ApplicationFactory(
        application=Application,
        controller=Controller,

        item_service=ItemService,
        review_service=ReviewService,
        category_service=CategoryService,

        item_repository=ItemRepository,
        category_repository=CategoryRepository,
        review_repository=ReviewRepository,

        app_config_path="tests/config/app_config.json",
        db_config_path="tests/config/db_config.json",
        urls_path="tests/config/urls.json"
    ).create()
    client = app.test_client()





