import psycopg2
from flask import make_response, Response, request

from user_service.services.service import AuthService
from user_service.storage.entities.serializers import UserSerializer

from user_service.exceptions import service_exceptions, repository_exceptions
from user_service.controllers.validators import (make_response_from_exception,
                                                 access_required,
                                                 permissions_required,
                                                 fields_required,
                                                 refresh_required)

# TODO: new permissions system


class AuthController:

    def __init__(self, service: AuthService, serializer: UserSerializer):
        self.service = service
        self.serializer = serializer

    @access_required
    def validate(self) -> Response:
        return make_response("200", 200)

    @access_required
    @permissions_required([])
    def validate_id(self, user_id) -> Response:
        return make_response("200", 200)

    def register(self) -> Response:
        # wrapper over default user creation
        return self.create()

    # wrapper over default admin creation
    def register_admin(self) -> Response:
        # wrapper over default user creation
        return self.create_admin()

    @fields_required(['email', 'password'])
    def authorize(self) -> Response:
        email = request.json['email']
        password = request.json['password']

        try:
            result = self.service.authorize(email, password)

        except (service_exceptions.PasswordDoesNotMatchError, repository_exceptions.UserNotFoundError) as err:
            return make_response_from_exception(err, 400, "Password or email are invalid")
        except (psycopg2.Error, repository_exceptions.PostgresConnError, Exception) as err:
            return make_response_from_exception(err, 500, "Unexpected error happened on the server")

        response = make_response("200", 200)
        response.set_cookie("access", result["access"])
        response.set_cookie("refresh", result["refresh"])
        return response

    @refresh_required
    def refresh(self) -> Response:
        refresh_token = request.cookies.get('refresh')
        result = self.service.refresh(refresh_token)

        response = make_response("200", 200)
        response.set_cookie("access", result["access"])
        return response

    @access_required
    @permissions_required(['GET SINGLE USER DATA'])
    def get(self, id_: int) -> Response:
        try:
            response = self.service.get(id_, True)

        except repository_exceptions.UserNotFoundError as err:
            return make_response_from_exception(err, 400, str(err))
        except (psycopg2.Error, repository_exceptions.PostgresConnError, Exception) as err:
            return make_response_from_exception(err, 500, "Unexpected error happened on the server")

        return make_response(self.serializer.serialize(response), 200)

    @access_required
    @permissions_required(['GET MULTIPLE USERS DATA'])
    def get_all(self) -> Response:
        try:
            responses = self.service.get_all(True)

        except (psycopg2.Error, repository_exceptions.PostgresConnError, Exception) as err:
            return make_response_from_exception(err, 500, "Unexpected error happened on the server")

        return make_response([self.serializer.serialize(response) for response in responses], 200)

    @fields_required(['email', 'password'])
    def create(self) -> Response:
        user = self.serializer.deserialize({"email": request.json["email"],
                                           "password": request.json["password"]})
        # role_id = 0 -- "User" role
        try:
            id_ = self.service.create(user, role_id=0)

        except (repository_exceptions.UniqueConstraintError, service_exceptions.PasswordException,
                service_exceptions.EmailException) as err:
            return make_response_from_exception(err, 400, str(err))
        except (psycopg2.Error, repository_exceptions.PostgresConnError, Exception) as err:
            return make_response_from_exception(err, 500, "Unexpected error happened on the server")

        return make_response(str(id_), 200)

    @access_required
    @fields_required(['email', 'password'])
    @permissions_required(['CREATE ADMIN'])
    def create_admin(self) -> Response:
        admin = self.serializer.deserialize({"email": request.json["email"],
                                            "password": request.json["password"]})
        # role_id = 1 -- "Admin" role
        try:
            id_ = self.service.create(admin, role_id=1)

        except (repository_exceptions.UniqueConstraintError, service_exceptions.PasswordException) as err:
            return make_response_from_exception(err, 400, str(err))
        except (psycopg2.Error, repository_exceptions.PostgresConnError, Exception) as err:
            return make_response_from_exception(err, 500, "Unexpected error happened on the server")

        return make_response(str(id_), 200)

    @access_required
    def delete(self, id_: int) -> Response:
        try:
            self.service.delete(id_)

        except repository_exceptions.UserNotFoundError as err:
            return make_response_from_exception(err, 400, str(err))
        except (psycopg2.Error, repository_exceptions.PostgresConnError, Exception) as err:
            return make_response_from_exception(err, 500, "Unexpected error happened on the server")

        return make_response("200", 200)

    @access_required
    def update(self, id_: int) -> Response:
        user = self.serializer.deserialize({"email": request.json["email"],
                                           "password": request.json["password"]})

        try:
            self.service.update(id_, user)

        except repository_exceptions.UserNotFoundError as err:
            return make_response_from_exception(err, 400, str(err))
        except (psycopg2.Error, repository_exceptions.PostgresConnError, Exception) as err:
            return make_response_from_exception(err, 500, "Unexpected error happened on the server")

        return make_response("200", 200)

    @access_required
    def get_user_role(self, id_: int) -> Response:
        try:
            role = self.service.get_user_role(id_)

        except repository_exceptions.RoleNotFoundError as err:
            return make_response_from_exception(err, 400, str(err))
        except (psycopg2.Error, repository_exceptions.PostgresConnError, Exception) as err:
            return make_response_from_exception(err, 500, "Unexpected error happened on the server")

        return make_response(role, 200)

    @access_required
    def get_user_permissions(self, id_: int) -> Response:
        try:
            permissions = self.service.get_user_permissions(id_)

        except repository_exceptions.PermissionsNotFoundError as err:
            return make_response_from_exception(err, 400, str(err))
        except (psycopg2.Error, repository_exceptions.PostgresConnError, Exception) as err:
            return make_response_from_exception(err, 500, "Unexpected error happened on the server")

        return make_response(permissions, 200)

