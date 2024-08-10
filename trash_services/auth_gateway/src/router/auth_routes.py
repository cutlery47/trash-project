from fastapi import APIRouter, Request, Response

from src.router.router import Router
from src.schema.user import AuthUser


def register_auth_routes(router: Router):

    @router.api.get("/refresh/")
    async def refresh(request: Request, response: Response):
        router.controller.refresh(request, response)

    @router.api.post("/authorize/")
    async def authorize(user: AuthUser, response: Response):
        router.controller.authorize(email=user.email,
                                    password=user.password,
                                    response=response)