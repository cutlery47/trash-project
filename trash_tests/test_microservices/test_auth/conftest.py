import json

import pytest
from flask import Flask

from auth_service.interfaces.factory_interface import FactoryInterface
from logging.config import dictConfig

from auth_service.storage.entities.serializers import UserSerializer
from test_microservices.test_auth.mock.mock_repository import MockAuthRepository
from auth_service.services.auth_service import AuthService
from auth_service.services.handlers import TokenHandler, EmailHandler, PasswordHandler
from auth_service.controllers.auth_controller import AuthController
from auth_service.router.router import Router, register_routes


app_config = "config/app_config.json"
db_config = "config/db_config.json"
logger_config = "config/logger_config.json"
jwt_secret_path = "config/jwt_secret.txt"

user = json.load(open(db_config)).get('USER')
dbname = json.load(open(db_config)).get('DBNAME')
setup_path = "migrations/setup/"
teardown_path = "migrations/teardown/"


# noinspection PyShadowingNames
class TestTrashFactory(FactoryInterface):
    @classmethod
    def create(cls, app_config, db_config, logger_config, jwt_secret_path) -> Flask:
        app = Flask(__name__)
        app.config.from_file(app_config, load=json.load)
        app.secret_key = open(jwt_secret_path).read()

        mock_repository = MockAuthRepository()
        service = AuthService(repository=mock_repository, token_handler=TokenHandler(), email_handler=EmailHandler(), password_handler=PasswordHandler())
        controller = AuthController(service=service, serializer=UserSerializer())
        router = Router("router", __name__, url_prefix="/api/v1/auth", controller=controller)

        with open(logger_config) as f:
            dictConfig(json.load(f))

        register_routes(router)
        app.register_blueprint(router)

        return app



@pytest.fixture(scope='session')
def app():
    app = TestTrashFactory.create(
        app_config=app_config,
        db_config=db_config,
        logger_config=logger_config,
        jwt_secret_path=jwt_secret_path,
    )
    app.testing = True

    yield app

@pytest.fixture()
def client(app):
    return app.test_client()
