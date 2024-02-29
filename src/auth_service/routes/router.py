from flask import Blueprint, request

from src.auth_service.controllers.signup_controller import SignUpController

router = Blueprint("routes", __name__, url_prefix="/api/v1/auth")


@router.post("/signup")
def signup():
    return SignUpController(request).handle()
