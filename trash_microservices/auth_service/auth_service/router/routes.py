from auth_service.router.router import Router


def register_auth_routes(router: Router):

    @router.post("/validate_access/")
    # validates jwt access token when requesting resources
    def validate_access_token():
        return router.controller.validate_access_token()

    @router.post("/validate_access/<int:user_id>")
    # validates access to a particular resource
    def validate_access_to_id(user_id):
        return router.controller.validate_access_to_id(user_id)

    @router.post("/validate_admin/")
    # validates that user has admin permissions
    def validate_admin():
        return router.controller.validate_admin()

    @router.post("/validate_access_and_admin/")
    # validates access token and then validates admin permissions
    def validate_access_and_admin():
        return router.controller.validate_access_and_admin()

    @router.post("/validate_access_and_id/<int:user_id>")
    # validates access token and then validated access to a resource
    def validate_access_and_id(user_id):
        return router.controller.validate_access_and_id(user_id)

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
    # returns user auth_service-info specified by id
    def get_user(user_id):
        return router.controller.get(user_id)

    @router.get("/users/")
    # returns all users auth_service-info
    def get_all_users():
        return router.controller.get_all()

    @router.delete("/users/<int:user_id>")
    # deletes user by specified id
    def delete_user(user_id):
        return router.controller.delete(user_id)

    @router.put("/users/<int:user_id>")
    # updates users data by their id
    def update_user(user_id):
        return router.controller.update(user_id)