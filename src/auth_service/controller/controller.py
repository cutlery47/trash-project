from flask import Blueprint

controller = Blueprint("controller", __name__, url_prefix="/api/v1/auth")


@controller.post("/login")
def log_in_controller():
    return '123123'


@controller.post("/signup")
def sign_up_controller():
    return '123123'


@controller.get("/perms/<int:user_id>")
def permissions_controller():
    return 'somesome'


@controller.get("/roles/<int:user_id>")
def roles_controller():
    return 'smth'

@controller.delete("<int:user_id>")
def auth_delete_controller():
    return "deleted"