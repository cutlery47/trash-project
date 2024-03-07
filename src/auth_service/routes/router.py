from flask import Blueprint, request, g
import logging

from src.auth_service.controllers.user_controller import UserController

router = Blueprint("routes", __name__, url_prefix="/api/v1/auth")


@router.before_request
def setup():
    g.logger = logging.getLogger(__name__)
    g.logger.info(f"Entering {request.path}")


@router.get("/users/get/<int:user_id>")
def get_user(user_id):
    return UserController(request).handle_get(user_id)


@router.get("/users/get/")
def get_all_users():
    return UserController(request).handle_get_all()
