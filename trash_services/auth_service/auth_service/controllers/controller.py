from flask import make_response, Response, request

from auth_service.services.service import AuthService
from auth_service.storage.entities.entities import User
from auth_service.validators.decorators import (access_required,
                                                admin_required,
                                                id_access_required,
                                                fields_required,
                                                refresh_required)


class AuthController:

    def __init__(self, service: AuthService):
        self.service = service

    @access_required
    def validate_access_token(self) -> Response:
        return make_response("200", 200)

    @admin_required
    def validate_admin(self) -> Response:
        return make_response("200", 200)

    @id_access_required
    def validate_access_to_id(self, user_id) -> Response:
        return make_response("200", 200)

    @access_required
    @admin_required
    def validate_access_and_admin(self) -> Response:
        return make_response("200", 200)

    @access_required
    @id_access_required
    def validate_access_and_id(self, user_id) -> Response:
        return make_response("200", 200)

    @fields_required(['email', 'password'])
    def authorize(self) -> Response:
        email = request.json['email']
        password = request.json['password']

        authorized_user_data = self.service.authorize(email, password)

        response = make_response("Authorized", 200)
        response.set_cookie("access", authorized_user_data["access"])
        response.set_cookie("refresh", authorized_user_data["refresh"])
        return response

    @refresh_required
    def refresh(self) -> Response:
        refresh_token = request.cookies.get('refresh')
        result = self.service.refresh_access_token(refresh_token)

        response = make_response("200", 200)
        response.set_cookie("access", result["access"])
        return response

    @access_required
    def get(self, id_: int) -> Response:
        user = self.service.get(id_=id_, is_secure=True)
        return make_response(user.serialize(), 200)

    @access_required
    def get_all(self) -> Response:
        users = self.service.get(is_secure=True)
        return make_response([user.serialize() for user in users], 200)

    @fields_required(['email', 'password'])
    def create_user(self) -> Response:
        user = User(email=request.json["email"], password=request.json["password"], role="user")
        created_user = self.service.create(user)
        return make_response(created_user.serialize(is_secure=True), 200)

    @access_required
    @admin_required
    @fields_required(['email', 'password'])
    def create_admin(self) -> Response:
        admin = User(email=request.json["email"], password=request.json["password"], role="admin")
        created_admin = self.service.create(admin)
        return make_response(created_admin.serialize(is_secure=True), 200)

    @access_required
    @id_access_required
    def delete(self, id_: int) -> Response:
        self.service.delete(id_)
        return make_response("200", 200)

    @access_required
    @id_access_required
    def update(self, id_: int) -> Response:
        user = User(email=request.json['email'], password=request.json['password'])
        self.service.update(id_, user)
        return make_response("200", 200)

