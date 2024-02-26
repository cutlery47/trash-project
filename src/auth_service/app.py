from flask import Flask, Blueprint
from controller.controller import controller

def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_pyfile('../../config/app_config.cfg')

    app.register_blueprint(controller)

    return app


if __name__ == "__main__":
    trash = create_app()
    trash.run(host="0.0.0.0", port=9876)

