from flask import Flask, Blueprint


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_pyfile('../../config/app_config.cfg')

    return app


if __name__ == "__main__":
    trash = create_app()
    trash.run(host="0.0.0.0", port=9876)

