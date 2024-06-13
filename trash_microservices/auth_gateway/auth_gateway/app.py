from flask import Flask
import json

from auth_gateway.storage.repositories.repository import AuthRepository
from auth_gateway.controllers.controller import AuthController
from auth_gateway.services.service import AuthService
from auth_gateway.router.router import Router
from auth_gateway.router.auth_routes import register_auth_routes
from auth_gateway.router.item_routes import register_item_routes

from auth_gateway.storage.repositories.query_builder import QueryBuilder
from auth_gateway.config.database.db_config import DBConfig
from auth_gateway.services.handlers import TokenHandler, EmailHandler, PasswordHandler
from auth_gateway.storage.entities.serializers import UserSerializer

from auth_gateway.interfaces.factory_interface import FactoryInterface


class TrashFactory(FactoryInterface):

    @classmethod
    def create(cls, app_config, db_config, jwt_secret_path) -> Flask:
        # configuring application
        app = Flask(__name__)
        app.config.from_file(app_config, load=json.load)
        app.secret_key = open(jwt_secret_path).read()

        repository = AuthRepository(config=DBConfig(db_config), query_builder=QueryBuilder())
        service = AuthService(repository=repository, email_handler=EmailHandler(), password_handler=PasswordHandler(),
                              token_handler=TokenHandler())
        controller = AuthController(service=service, serializer=UserSerializer())
        router = Router("router", __name__, url_prefix="/api/v1/", controller=controller)

        # routing
        register_auth_routes(router)
        register_item_routes(router)
        app.register_blueprint(router)

        return app


if __name__ == "__main__":
    trash = TrashFactory.create(
        app_config="config/app/app_config.json",
        db_config="auth_gateway/config/database/db_config.json",
        jwt_secret_path="auth_gateway/config/app/jwt_secret.txt"
    )

    trash.run(host="0.0.0.0", port=9876)
