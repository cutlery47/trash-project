from fastapi import FastAPI

from src.config.database.db_config import DBConfig

from src.storage.repositories.repository import AuthRepository
from src.storage.repositories.query_builder import CRUDQueryBuilder

from src.service.service import AuthService

from src.service.token_generator import TokenGenerator
from src.service.password_hasher import PasswordHasher

from src.validators.token_validator import TokenValidator
from src.validators.input_validator import InputValidator
from src.validators.credentials_validator import CredentialsValidator

from src.controller.controller import AuthController

from src.router.router import Router
from src.router.auth_routes import register_auth_routes
from src.router.item_service_routes import register_item_routes
from src.router.user_service_routes import register_user_routes

from src.application.application import Application

class ApplicationFactory:

    @classmethod
    def create(cls, db_config_path: str) -> Application:

        repository = AuthRepository(config=DBConfig(db_config_path),
                                    query_builder=CRUDQueryBuilder())

        service = AuthService(repository=repository,
                              token_generator=TokenGenerator(),
                              password_hasher=PasswordHasher())

        controller = AuthController(service=service,
                                    token_validator=TokenValidator(),
                                    input_validator=InputValidator(),
                                    credentials_validator=CredentialsValidator())

        router = Router(url_prefix="/api/v1",
                        controller=controller)

        register_auth_routes(router)
        register_user_routes(router)
        register_item_routes(router)

        application = Application(router)

        return application
