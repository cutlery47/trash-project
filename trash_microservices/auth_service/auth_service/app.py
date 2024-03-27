from flask import Flask
import json

from auth_service.storage.repositories.auth_repository import Repository
from auth_service.services.auth_service import Service
from auth_service.controllers.auth_controller import Controller
from auth_service.router.router import Router, register_routes


class TrashAssApplication:

    @classmethod
    def create(cls,
               app_config="config/app/app_config.json",
               db_config="auth_service/config/database/db_config.json"
               ) -> Flask:

        # configuring application
        app = Flask(__name__)
        app.config.from_file(app_config, load=json.load)

        repo = Repository(db_config)
        service = Service(repo=repo)
        controller = Controller(service=service)
        router = Router("router", __name__, url_prefix="/api/v1/auth", controller=controller)

        # routing
        register_routes(router)
        app.register_blueprint(router)

        return app


if __name__ == "__main__":
    trash = TrashAssApplication.create()
    trash.run(host="0.0.0.0", port=9876)
