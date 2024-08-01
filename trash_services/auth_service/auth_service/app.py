from flask import Flask
import json

from auth_service.router.router import Router
from auth_service.router.routes import register_auth_routes

from auth_service.controllers.controller import AuthController

from auth_service.services.service import AuthService
from auth_service.services.token_generator import TokenGenerator
from auth_service.services.password_hasher import PasswordHasher

from auth_service.validators.token_validator import TokenValidator
from auth_service.validators.credentials_validator import CredentialsValidator

from auth_service.storage.repositories.repository import AuthRepository
from auth_service.storage.repositories.query_builder import CRUDQueryBuilder

from auth_service.exceptions.exception_handlers import register_exception_handlers
from auth_service.config.database.db_config import DBConfig
from auth_service.interfaces.factory_interface import FactoryInterface


class TrashFactory(FactoryInterface):

    @classmethod
    def create(cls, app_config, db_config, jwt_secret_path, is_testing: bool = False) -> Flask:

        app = Flask(__name__)
        app.testing = is_testing

        # Configuring the application
        app.config.from_file(app_config, load=json.load)
        app.secret_key = open(jwt_secret_path).read()

        # Creating and injecting components
        repository = AuthRepository(config=DBConfig(db_config),
                                    query_builder=CRUDQueryBuilder())

        service = AuthService(repository=repository,
                              token_generator=TokenGenerator(),
                              token_validator=TokenValidator(),
                              password_hasher=PasswordHasher(),
                              credentials_validator=CredentialsValidator())

        controller = AuthController(service=service)

        router = Router("router", __name__,
                        url_prefix="/api/v1/",
                        controller=controller)

        # Creating server endpoints and assigning them to the application
        register_auth_routes(router)
        app.register_blueprint(router)

        register_exception_handlers(app)

        return app


if __name__ == "__main__":

    trash = TrashFactory.create(
        app_config="config/app/app_config.json",
        db_config="auth_service/config/database/db_config.json",
        jwt_secret_path="auth_service/config/app/jwt_secret.txt"
    )

    trash.run(host="0.0.0.0", port=9876)
