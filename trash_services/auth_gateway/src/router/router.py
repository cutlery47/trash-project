from fastapi import APIRouter

from src.controller.controller import AuthController

class Router:

    def __init__(self, url_prefix: str, controller: AuthController):
        self.api = APIRouter(prefix=url_prefix)
        self.controller = controller

