from fastapi import APIRouter, Request, Response

from src.controller.controller import AuthController
from src.schema.user import AuthUser, InUser, UpdateUser
from src.exceptions.validation_exceptions import ValidationException

class Router:

    def __init__(self, url_prefix: str, controller: AuthController):
        self.router = APIRouter(prefix=url_prefix)
        self.controller = controller
        self._register_auth_routes()

    def _register_auth_routes(self):

        @self.router.get("/items/")
        async def refresh(request: Request):
            self.controller.refresh(request)

        @self.router.get("/refresh/")
        async def refresh(request: Request, response: Response):
            self.controller.refresh(request, response)

        @self.router.post("/authorize/")
        async def authorize(user: AuthUser, response: Response):
            self.controller.authorize(email=user.email,
                                             password=user.password,
                                             response=response)

        @self.router.post("/register/")
        async def register(user: InUser):
            return self.controller.create(**user.model_dump(), role="user")

        @self.router.post("/register_admin/")
        async def register_admin(request: Request, admin: InUser):
            self.controller.validate_admin(request)
            return self.controller.create(**admin.model_dump(), role="admin")

        @self.router.get("/users/")
        async def get_all_users():
            return self.controller.get_all()

        @self.router.get("/users/{user_id}")
        async def get_user(user_id: int):
            return self.controller.get(user_id)

        @self.router.delete("/users/{user_id}")
        async def delete_user(request: Request, user_id: int):
            try:
                self.controller.validate_access_to_id(request, user_id)
            except ValidationException as exc:
                self.controller.validate_admin(request)
                raise exc
            self.controller.delete(user_id)

        @self.router.put("/users/{user_id}")
        async def update_user(user: UpdateUser, request: Request, user_id: int):
            try:
                self.controller.validate_access_to_id(request, user_id)
            except ValidationException as exc:
                self.controller.validate_admin(request)
                raise exc
            self.controller.update(id_=user_id, **user.model_dump())



