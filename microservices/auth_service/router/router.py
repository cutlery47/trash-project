from flask import Blueprint, request

from src.auth_service.controllers.user_controller import UserController


class Router(Blueprint):
    def __init__(self, name, import_name, url_prefix, controller: UserController):
        super().__init__(name, import_name, url_prefix=url_prefix)
        self.controller = controller


def register_routes(router: Router):
    @router.get("/users/get/<int:user_id>")
    def get_user(user_id):
        return router.controller.get(user_id)

    @router.get("/users/get/")
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