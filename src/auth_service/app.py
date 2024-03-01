from flask import Flask
from routes.router import router
import json


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_file("config/app_config.json", load=json.load)

    app.register_blueprint(router)

    return app


if __name__ == "__main__":
    trash = create_app()
    trash.run(host="0.0.0.0", port=9876)
