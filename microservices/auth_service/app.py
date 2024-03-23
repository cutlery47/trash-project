from flask import Flask
import json

from microservices.auth_service.storage.repositories.auth_repository import UserRepository
from microservices.auth_service.services.auth_service import UserService
from microservices.auth_service.controllers.auth_controller import UserController
from microservices.auth_service.router.router import Router, register_routes


class TrashAssApplication:

    @classmethod
    def create(cls,
               app_config="config/app/app_config.json",
               db_config="microservices/auth_service/config/database/db_config.json"
               ) -> Flask:

        # configuring application
        app = Flask(__name__)
        app.config.from_file(app_config, load=json.load)

        repo = UserRepository(db_config)
        service = UserService(repo=repo)
        controller = UserController(service=service)
        router = Router("router", __name__, url_prefix="/api/v1/auth", controller=controller)

        # routing
        register_routes(router)
        app.register_blueprint(router)

        return app


if __name__ == "__main__":
    trash = TrashAssApplication.create()
    trash.run(host="0.0.0.0", port=9876)
