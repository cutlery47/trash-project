from flask import Blueprint

from auth_service.controllers.controller import AuthController

class Router(Blueprint):
    def __init__(self, name, import_name, url_prefix, controller: AuthController):
        super().__init__(name, import_name, url_prefix=url_prefix)
        self.controller = controller
