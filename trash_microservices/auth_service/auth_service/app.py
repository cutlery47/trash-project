from flask import Flask
from logging.config import dictConfig
import json

from auth_service.storage.repositories.auth_repository import AuthRepository
from auth_service.controllers.auth_controller import AuthController
from auth_service.services.auth_service import AuthService
from auth_service.router.router import Router, register_routes

from auth_service.storage.repositories.query_builder import QueryBuilder
from auth_service.config.database.db_config import DBConfig
from auth_service.services.handlers import TokenHandler, EmailHandler, PasswordHandler
from auth_service.storage.entities.serializers import UserSerializer

from auth_service.interfaces.factory_interface import FactoryInterface


class TrashFactory(FactoryInterface):

    @classmethod
    def create(cls, app_config, db_config, logger_config, jwt_secret_path) -> Flask:
        # configuring application
        app = Flask(__name__)
        app.config.from_file(app_config, load=json.load)
        app.secret_key = open(jwt_secret_path).read()

        repository = AuthRepository(config=DBConfig(db_config), query_builder=QueryBuilder())
        service = AuthService(repository=repository, email_handler=EmailHandler(), password_handler=PasswordHandler(), token_handler=TokenHandler())
        controller = AuthController(service=service, serializer=UserSerializer())
        router = Router("router", __name__, url_prefix="/api/v1/auth", controller=controller)

        # configuring logger
        with open(logger_config) as f:
            dictConfig(json.load(f))

        # routing
        register_routes(router)
        app.register_blueprint(router)

        return app


if __name__ == "__main__":
    trash = TrashFactory.create(
        app_config="config/app/app_config.json",
        db_config="auth_service/config/database/db_config.json",
        logger_config="auth_service/config/app/logger_config.json",
        jwt_secret_path="auth_service/config/app/jwt_secret.txt"
    )

    trash.run(host="0.0.0.0", port=9876)
