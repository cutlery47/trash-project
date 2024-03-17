from flask import Blueprint

from microservices.auth_service.controllers.auth_user_controller import UserController


class Router(Blueprint):
    def __init__(self, name, import_name, url_prefix, controller: UserController):
        super().__init__(name, import_name, url_prefix=url_prefix)
        self.controller = controller


def register_routes(router: Router):
    @router.post("/register/")
    def register_user():
        return router.controller.register()

    @router.post("/register_admin/")
    def register_admin():
        return router.controller.register_admin()

    @router.post("/login/")
    def login():
        return router.controller.login()

    @router.get("/users/<int:user_id>")
    def get_user(user_id):
        return router.controller.get(user_id)

    @router.get("/users/")
    def get_all_users():
        return router.controller.get_all()

    @router.post("/users/create/")
    def create_user():
        return router.controller.create()

    @router.post("/users/create_admin/")
    def create_admin():
        return router.controller.create_admin()

    @router.delete("/users/delete/<int:user_id>")
    def delete_user(user_id):
        return router.controller.delete(user_id)

    @router.put("/users/update/<int:user_id>")
    def update_user(user_id):
        return router.controller.update(user_id)

    @router.get("/users/role/<int:user_id>")
    def get_user_role(user_id):
        return router.controller.get_user_role(user_id)

    @router.get("/users/permissions/<int:user_id>")
    def get_user_permissions(user_id):
        return router.controller.get_user_permissions(user_id)