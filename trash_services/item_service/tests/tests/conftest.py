from item_service.application.factory import ApplicationFactory
from item_service.application.application import Application

from item_service.controller.controller import Controller
from item_service.controller.handlers.validator import RequestValidator

from item_service.services.services.item_service import ItemService
from item_service.services.services.review_service import ReviewService
from item_service.services.services.category_service import CategoryService

from item_service.repositories.repositories.item_repository import ItemRepository
from item_service.repositories.repositories.review_repository import ReviewRepository
from item_service.repositories.repositories.category_repository import CategoryRepository
from item_service.repositories.handlers.exception_handler import RepositoryExceptionHandler

from item_service.cache.redis_client import RedisClient
from item_service.cache.redis_client_factory import RedisClientFactory
from redis.asyncio.connection import ConnectionPool

from item_service.config.database.db_config import DBConfig

from httpx import AsyncClient, Cookies
import httpx

from alembic.config import Config
from alembic import command

from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database, drop_database

import json
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

@pytest.fixture(scope="module")
def app(apply_migrations) -> Application:
    app = ApplicationFactory(
        application_class=Application,
        controller_class=Controller,

        item_service_class=ItemService,
        review_service_class=ReviewService,
        category_service_class=CategoryService,

        request_validator_class=RequestValidator,

        item_repository_class=ItemRepository,
        category_repository_class=CategoryRepository,
        review_repository_class=ReviewRepository,

        repository_exc_handler_class=RepositoryExceptionHandler,

        app_config_path="tests/config/app_config.json",
        db_config_path="tests/config/db_config.json",
        urls_path="tests/config/urls.json",

        cache_config_path="tests/config/cache_config.json",
        cache_connection_pool_class=ConnectionPool,
        cache_client_factory_class=RedisClientFactory
    ).create()
    yield app

@pytest.fixture(scope="module")
def client(app) -> AsyncClient:
    yield app.async_test_client()

@pytest.fixture(scope="module")
def user_id(app) -> int:
    re = httpx.post(url=urls_dict['/register/'],
                    headers=headers,
                    json={"email": email, "password": password})

    yield int(re.text)

    httpx.delete(url=urls_dict['/users/'] + re.text,
                 cookies=re.cookies,
                 headers=headers)

@pytest.fixture(scope="module")
def cookies(app) -> Cookies:
    re = httpx.post(url=urls_dict['/authorize/'],
                    headers=headers,
                    json={"email": email, "password": password})
    return re.cookies

