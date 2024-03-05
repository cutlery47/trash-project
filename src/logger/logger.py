import logging.config
import logging.handlers
import logging
import atexit
import json

config_path = "logger_config.json"


class Logger:

    def __init__(self):
        self._logger = logging.getLogger(__name__)
        logging.config.dictConfig(json.load(open(config_path)))
        queue_handler = logging.getHandlerByName("queue_handler")
        if queue_handler is not None:
            queue_handler.listener.start()
            atexit.register(queue_handler.listener.stop)


    def debug(self, msg):
        self._logger.debug(msg)


logger = Logger()
for i in range(10):
    logger.debug('123fds123')