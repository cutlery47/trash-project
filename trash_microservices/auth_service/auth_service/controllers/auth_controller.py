import psycopg2
from flask import make_response, Response, request

from auth_service.services.auth_service import Service
from auth_service.storage.entities.serializers import UserSerializer

from auth_service.exceptions import service_exceptions, repository_exceptions
from auth_service.controllers.validators import (make_response_from_exception,
                                                 authentication_required,
                                                 permissions_required,
                                                 fields_required,
                                                 refresh_required)


class Controller:

    def __init__(self, service: Service):
        self.service = service
        self.serializer = UserSerializer()

    @authentication_required
    def validate(self) -> Response:
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

        return make_response(result, 200)

    @refresh_required
    def refresh(self) -> Response:
        refresh_token = request.json['refresh']
        new_access_token = self.service.refresh(refresh_token)

        return make_response(new_access_token, 200)

    @authentication_required
    @permissions_required(['GET SINGLE USER DATA'])
    def get(self, id_: int) -> Response:
        try:
            response = self.service.get(id_, True)

        except repository_exceptions.UserNotFoundError as err:
            return make_response_from_exception(err, 400, str(err))
        except (psycopg2.Error, repository_exceptions.PostgresConnError, Exception) as err:
            return make_response_from_exception(err, 500, "Unexpected error happened on the server")

        return make_response(self.serializer.serialize(response), 200)

    @authentication_required
    @permissions_required(['GET MULTIPLE USERS DATA'])
    def get_all(self) -> Response:
        try:
            responses = self.service.get_all(True)

        except (psycopg2.Error, repository_exceptions.PostgresConnError, Exception) as err:
            return make_response_from_exception(err, 500, "Unexpected error happened on the server")

        return make_response([UserSerializer.serialize(response) for response in responses], 200)

    @fields_required(['email', 'password'])
    def create(self) -> Response:
        user = UserSerializer.deserialize({"email": request.json["email"],
                                           "password": request.json["password"]})
        try:
            self.service.create(user)

        except repository_exceptions.UniqueConstraintError as err:
            return make_response_from_exception(err, 400, str(err))
        except (psycopg2.Error, repository_exceptions.PostgresConnError, Exception) as err:
            return make_response_from_exception(err, 500, "Unexpected error happened on the server")

        return make_response("200", 200)

    @authentication_required
    @fields_required(['email', 'password'])
    @permissions_required(['CREATE ADMIN'])
    def create_admin(self) -> Response:
        admin = UserSerializer.deserialize({"email": request.json["email"],
                                           "password": request.json["password"]})
        try:
            self.service.create_admin(admin)

        except repository_exceptions.UniqueConstraintError as err:
            return make_response_from_exception(err, 400, str(err))
        except (psycopg2.Error, repository_exceptions.PostgresConnError, Exception) as err:
            return make_response_from_exception(err, 500, "Unexpected error happened on the server")

        return make_response("200", 200)

    @authentication_required
    @permissions_required(['DELETE ANY USER'])
    def delete(self, id_: int) -> Response:
        try:
            self.service.delete(id_)

        except repository_exceptions.UserNotFoundError as err:
            return make_response_from_exception(err, 400, str(err))
        except (psycopg2.Error, repository_exceptions.PostgresConnError, Exception) as err:
            return make_response_from_exception(err, 500, "Unexpected error happened on the server")

        return make_response("200", 200)

    @authentication_required
    @permissions_required(['UPDATE ANY USER DATA'])
    def update(self, id_: int) -> Response:
        user = UserSerializer.deserialize({"email": request.json["email"],
                                           "password": request.json["password"]})

        try:
            self.service.update(id_, user)

        except repository_exceptions.UserNotFoundError as err:
            return make_response_from_exception(err, 400, str(err))
        except (psycopg2.Error, repository_exceptions.PostgresConnError, Exception) as err:
            return make_response_from_exception(err, 500, "Unexpected error happened on the server")

        return make_response("200", 200)

    @authentication_required
    @permissions_required(['GET ANY USER ROLE'])
    def get_user_role(self, id_: int) -> Response:
        try:
            role = self.service.get_user_role(id_)

        except repository_exceptions.RoleNotFoundError as err:
            return make_response_from_exception(err, 400, str(err))
        except (psycopg2.Error, repository_exceptions.PostgresConnError, Exception) as err:
            return make_response_from_exception(err, 500, "Unexpected error happened on the server")

        return make_response(role, 200)

    @authentication_required
    @permissions_required(['GET ANY USER PERMISSION'])
    def get_user_permissions(self, id_: int) -> Response:
        try:
            permissions = self.service.get_user_permissions(id_)

        except repository_exceptions.PermissionsNotFoundError as err:
            return make_response_from_exception(err, 400, str(err))
        except (psycopg2.Error, repository_exceptions.PostgresConnError, Exception) as err:
            return make_response_from_exception(err, 500, "Unexpected error happened on the server")

        return make_response(permissions, 200)

