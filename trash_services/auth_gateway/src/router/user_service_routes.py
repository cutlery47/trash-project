from fastapi import Request

from src.router.router import Router
from src.schema.user import InUser, UpdateUser
from src.exceptions.validation_exceptions import ValidationException

def register_user_routes(router: Router):

    @router.api.post("/register/")
    async def register(user: InUser):
        return router.controller.create(**user.model_dump(), role="user")

    @router.api.post("/register_admin/")
    async def register_admin(request: Request, admin: InUser):
        router.controller.validate_admin(request)
        return router.controller.create(**admin.model_dump(), role="admin")

    @router.api.get("/users/")
    async def get_all_users(request: Request):
        router.controller.validate_access_token(request)
        return router.controller.get_all()

    @router.api.get("/users/{user_id}")
    async def get_user(user_id: int, request: Request):
        router.controller.validate_access_token(request)
        return router.controller.get(user_id)

    @router.api.delete("/users/{user_id}")
    async def delete_user(request: Request, user_id: int):
        token = router.controller.validate_access_token(request)

        try:
            router.controller.validate_admin(request, token)
        except ValidationException:
            router.controller.validate_access_to_id(request, user_id, token)

        router.controller.delete(user_id)

    @router.api.put("/users/{user_id}")
    async def update_user(user: UpdateUser, request: Request, user_id: int):
        token = router.controller.validate_access_token(request)

        try:
            token = router.controller.validate_admin(request, token)
        except ValidationException:
            router.controller.validate_access_to_id(request, user_id, token)

        router.controller.update(id_=user_id, **user.model_dump())

