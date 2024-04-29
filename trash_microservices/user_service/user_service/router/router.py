from flask import Blueprint

from auth_service.controllers.controller import AuthController


class Router(Blueprint):
    def __init__(self, name, import_name, url_prefix, controller: AuthController):
        super().__init__(name, import_name, url_prefix=url_prefix)
        self.controller = controller


def register_routes(router: Router):
    @router.post("/validate/")
    # validates jwt access token when requesting resources
    def validate():
        return router.controller.validate()

    @router.post("/register/")
    # creates a new user
    def register_user():
        return router.controller.register()

    @router.post("/register_admin/")
    # creates a new admin
    def register_admin():
        return router.controller.register_admin()

    @router.post("/authorize/")
    # authenticates user and returns a pair of access + refresh tokens
    def authorize():
        return router.controller.authorize()

    @router.post("/refresh/")
    # refreshes access token, if refresh token is valid
    def refresh():
        return router.controller.refresh()

    @router.get("/users/<int:user_id>")
    # returns user user_service-info specified by id
    def get_user(user_id):
        return router.controller.get(user_id)

    @router.get("/users/")
    # returns all users user_service-info
    def get_all_users():
        return router.controller.get_all()

    @router.delete("/users/delete/<int:user_id>")
    # deletes user by specified id
    def delete_user(user_id):
        return router.controller.delete(user_id)

    @router.put("/users/update/<int:user_id>")
    # updates users data by their id
    def update_user(user_id):
        return router.controller.update(user_id)

    @router.get("/users/role/<int:user_id>")
    # returns users roles by their id
    def get_user_role(user_id):
        return router.controller.get_user_role(user_id)

    @router.get("/users/permissions/<int:user_id>")
    # returns users permissions by their id
    def get_user_permissions(user_id):
        return router.controller.get_user_permissions(user_id)