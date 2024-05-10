from flask import Flask
import json

from user_service.storage.repositories.repository import AuthRepository
from user_service.controllers.controller import AuthController
from user_service.services.service import AuthService
from user_service.router.router import Router, register_routes

from user_service.storage.repositories.query_builder import QueryBuilder
from user_service.config.database.db_config import DBConfig
from user_service.services.handlers import TokenHandler, EmailHandler, PasswordHandler
from user_service.storage.entities.serializers import UserSerializer

from user_service.interfaces.factory_interface import FactoryInterface


class TrashFactory(FactoryInterface):

    @classmethod
    def create(cls, app_config, db_config, jwt_secret_path) -> Flask:
        # configuring application
        app = Flask(__name__)
        app.config.from_file(app_config, load=json.load)
        app.secret_key = open(jwt_secret_path).read()

        repository = AuthRepository(config=DBConfig(db_config), query_builder=QueryBuilder())
        service = AuthService(repository=repository, email_handler=EmailHandler(), password_handler=PasswordHandler(), token_handler=TokenHandler())
        controller = AuthController(service=service, serializer=UserSerializer())
        router = Router("router", __name__, url_prefix="/api/v1/", controller=controller)

        # routing
        register_routes(router)
        app.register_blueprint(router)

        return app


if __name__ == "__main__":
    trash = TrashFactory.create(
        app_config="config/app/app_config.json",
        db_config="user_service/config/database/db_config.json",
        jwt_secret_path="user_service/config/app/jwt_secret.txt"
    )

    trash.run(host="0.0.0.0", port=9876)
