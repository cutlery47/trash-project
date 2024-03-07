from logging.config import dictConfig
from routes.router import router
from flask import Flask
import atexit
import logging
import json


class TrashAssApplication:
    logger_config = "config/logger/logger_config.json"
    app_config = "config/app/app_config.json"

    @classmethod
    def create(cls) -> Flask:
        # configuring logger
        dictConfig(json.load(open(cls.logger_config)))
        queue_handler = logging.getHandlerByName("queue_handler")
        if queue_handler is not None:
            queue_handler.listener.start()
            atexit.register(queue_handler.listener.stop)

        # configuring application
        app = Flask(__name__)
        app.config.from_file(cls.app_config, load=json.load)

        # routing
        app.register_blueprint(router)

        return app


if __name__ == "__main__":
    trash = TrashAssApplication.create()
    trash.run(host="0.0.0.0", port=9876)
