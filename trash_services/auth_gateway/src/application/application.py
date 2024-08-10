from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.router.router import Router

from typing import List

class Application:

    def __init__(self, *routers: Router):
        self._app = FastAPI()
        for router in routers:
            self._app.include_router(router.api)

    def asgi_app(self) -> FastAPI:
        return self._app

    def test_client(self) -> TestClient:
        return TestClient(app=self.asgi_app(), follow_redirects=True)
