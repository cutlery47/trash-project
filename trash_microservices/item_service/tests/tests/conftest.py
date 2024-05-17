from item_service.application.factory import ApplicationFactory
from item_service.application.application import Application
from item_service.controller.controller import Controller
from item_service.controller.validator import RequestValidator
from item_service.services.item_service import ItemService
from item_service.services.review_service import ReviewService
from item_service.services.category_service import CategoryService
from item_service.repositories.item_repository import ItemRepository
from item_service.repositories.review_repository import ReviewRepository
from item_service.repositories.category_repository import CategoryRepository
from item_service.config.db_config import DBConfig

from httpx import AsyncClient, Cookies

from alembic.config import Config
from alembic import command

from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database, drop_database

from loguru import logger

import json
import httpx
import pytest

app_config_path = "tests/config/app_config.json"
db_config_path = "tests/config/db_config.json"
migration_path = "tests/config/migration_config.json"
urls_path = "tests/config/urls.json"

email = "example_123@gmail.com"
password = "example_123_password"
headers = {"Content-Type": "application/json"}
urls_dict = json.load(open(urls_path))

@pytest.fixture(scope="session")
def create_db():
    db_config_dict = json.load(open(migration_path))
    db_config = DBConfig(**db_config_dict)
    alchemy_engine = create_engine(f"{db_config.driver}"
                                   f"://{db_config.username}:"
                                   f"{db_config.password}@"
                                   f"{db_config.host}:"
                                   f"{db_config.port}/"
                                   f"{db_config.dbname}")

    if not database_exists(alchemy_engine.url):
        create_database(alchemy_engine.url)
    yield
    drop_database(alchemy_engine.url)

@pytest.fixture(scope="session")
def apply_migrations(create_db):
    config = Config(Path.cwd() / "tests" / "alembic.ini")

    command.upgrade(config, "head")
    yield
    command.downgrade(config, "-1")

@pytest.fixture(scope="session")
def app(apply_migrations) -> Application:
    app = ApplicationFactory(
        application=Application,
        controller=Controller,

        item_service=ItemService,
        review_service=ReviewService,
        category_service=CategoryService,

        request_validator=RequestValidator,

        item_repository=ItemRepository,
        category_repository=CategoryRepository,
        review_repository=ReviewRepository,

        app_config_path="tests/config/app_config.json",
        db_config_path="tests/config/db_config.json",
        urls_path="tests/config/urls.json"
    ).create()

    yield app

@pytest.fixture(scope="session")
def client(app) -> AsyncClient:
    return app.async_test_client()

@pytest.fixture(scope="session")
def cookies(app) -> Cookies:
    re = httpx.post(url=urls_dict['/register/'], headers=headers,
                    json={"email": email, "password": password})
    user_id = re.text

    re = httpx.post(url=urls_dict['/authorize/'], headers=headers,
                    json={"email": email, "password": password})
    cookies = re.cookies

    yield cookies

    # cleanup
    httpx.delete(url=urls_dict['/users/'] + user_id, headers=headers)






