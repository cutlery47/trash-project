import psycopg2
from flask import make_response, Response, request

from microservices.auth_service.services.auth_service import UserService
from microservices.auth_service.storage.entities.serializers import UserSerializer

from microservices.auth_service.exceptions import repository_exceptions, controller_exceptions, service_exceptions
from microservices.auth_service.controllers.data_validators import (InputValidator, TokenValidator,
                                                                    PermissionValidator, make_response_from_exception)


class UserController:

    def __init__(self, service: UserService):
        self.service = service
        self.serializer = UserSerializer()
        self.input_validator = InputValidator()
        self.token_validator = TokenValidator()
        self.permission_validator = PermissionValidator()

    # wrapper over default user creation
    def register(self) -> Response:
        return self.create()

    # wrapper over default admin creation
    def register_admin(self) -> Response:
        return self.create_admin()

    def authorize(self) -> Response:
        input_validator_response = self.input_validator.validate_desired(desired_keys=['email', 'password'],
                                                                         json=request.json)
        if input_validator_response is not True:
            return input_validator_response

        email = request.json['email']
        password = request.json['password']

        try:
            result = self.service.authorize(email, password)

        except (service_exceptions.PasswordDoesNotMatchError, repository_exceptions.UserNotFoundError) as err:
            return make_response_from_exception(err, 400, "Password or email are invalid")
        except (psycopg2.Error, repository_exceptions.PostgresConnError, Exception) as err:
            return make_response_from_exception(err, 500, "Unexpected error happened on the server")

        return make_response(result, 200)

    def refresh(self) -> Response:
        # generates an access token by using the information provided in refresh token
        # (only if refresh token itself is valid)
        input_validator_response = self.input_validator.validate_desired(desired_keys=['refresh'],
                                                                         json=request.json)
        if input_validator_response is not True:
            return input_validator_response

        token_validator_response = self.token_validator.validate_refresh(request.json)

        if token_validator_response is not True:
            return token_validator_response

        refresh_token = request.json['refresh']
        new_access_token = self.service.refresh(refresh_token)

        return make_response(new_access_token, 200)

    def get(self, id_: int) -> Response:
        access_validation_response = self.token_validator.validate_access(json=request.json)

        if access_validation_response is not True:
            return access_validation_response

        permissions_validation_response = self.permission_validator.validate(permissions=['GET USER DATA'],
                                                                             json=request.json)
        if permissions_validation_response is not True:
            return permissions_validation_response

        try:
            response = self.service.get(id_, True)

        except repository_exceptions.UserNotFoundError as err:
            return make_response_from_exception(err, 400, str(err))
        except (psycopg2.Error, repository_exceptions.PostgresConnError, Exception) as err:
            return make_response_from_exception(err, 500, "Unexpected error happened on the server")

        return make_response(self.serializer.serialize(response), 200)

    def get_all(self) -> Response:
        access_validation_response = self.token_validator.validate_access(request.json)

        if access_validation_response is not True:
            return access_validation_response

        permissions_validation_response = self.permission_validator.validate(permissions=["GET MULTIPLE USERS DATA"],
                                                                             json=request.json)
        if permissions_validation_response is not True:
            return permissions_validation_response

        try:
            responses = self.service.get_all(True)

        except (psycopg2.Error, repository_exceptions.PostgresConnError, Exception) as err:
            return make_response_from_exception(err, 500, "Unexpected error happened on the server")

        return make_response([UserSerializer.serialize(response) for response in responses], 200)

    def create(self) -> Response:
        input_validator_response = self.input_validator.validate_desired(desired_keys=['email', 'password'],
                                                                         json=request.json)
        if input_validator_response is not True:
            return input_validator_response

        user = UserSerializer.deserialize({"email": request.json["email"],
                                           "password": request.json["password"]})

        try:
            self.service.create(user)

        except repository_exceptions.UniqueConstraintError as err:
            return make_response_from_exception(err, 400, str(err))
        except (psycopg2.Error, repository_exceptions.PostgresConnError, Exception) as err:
            return make_response_from_exception(err, 500, "Unexpected error happened on the server")

        return make_response("200", 200)

    def create_admin(self) -> Response:
        input_validator_response = self.input_validator.validate_desired(desired_keys=['email', 'password'],
                                                                         json=request.json)
        if input_validator_response is not True:
            return input_validator_response

        admin = UserSerializer.deserialize({"email": request.json["email"],
                                           "password": request.json["password"]})

        try:
            self.service.create_admin(admin)

        except repository_exceptions.UniqueConstraintError as err:
            return make_response_from_exception(err, 400, str(err))
        except (psycopg2.Error, repository_exceptions.PostgresConnError, Exception) as err:
            return make_response_from_exception(err, 500, "Unexpected error happened on the server")

        return make_response("200", 200)

    def delete(self, id_: int) -> Response:
        access_validation_response = self.token_validator.validate_access(request.json)

        # verification failed
        if access_validation_response is not True:
            return access_validation_response

        try:
            self.service.delete(id_)

        except repository_exceptions.UserNotFoundError as err:
            return make_response_from_exception(err, 400, str(err))
        except (psycopg2.Error, repository_exceptions.PostgresConnError, Exception) as err:
            return make_response_from_exception(err, 500, "Unexpected error happened on the server")

        return make_response("200", 200)

    def update(self, id_: int) -> Response:
        access_validation_response = self.token_validator.validate_access(request.json)

        # verification failed
        if access_validation_response is not True:
            return access_validation_response

        user = UserSerializer.deserialize({"email": request.json["email"],
                                           "password": request.json["password"]})

        try:
            self.service.update(id_, user)

        except repository_exceptions.UserNotFoundError as err:
            return make_response_from_exception(err, 400, str(err))
        except (psycopg2.Error, repository_exceptions.PostgresConnError, Exception) as err:
            return make_response_from_exception(err, 500, "Unexpected error happened on the server")

        return make_response("200", 200)

    def get_user_role(self, id_: int) -> Response:
        access_validation_response = self.token_validator.validate_access(request.json)

        # verification failed
        if access_validation_response is not True:
            return access_validation_response

        try:
            role = self.service.get_user_role(id_)

        except repository_exceptions.RoleNotFoundError as err:
            return make_response_from_exception(err, 400, str(err))
        except (psycopg2.Error, repository_exceptions.PostgresConnError, Exception) as err:
            return make_response_from_exception(err, 500, "Unexpected error happened on the server")

        return make_response(role, 200)

    def get_user_permissions(self, id_: int) -> Response:
        access_validation_response = self.token_validator.validate_access(request.json)

        # verification failed
        if access_validation_response is not True:
            return access_validation_response

        try:
            permissions = self.service.get_user_permissions(id_)

        except repository_exceptions.PermissionsNotFoundError as err:
            return make_response_from_exception(err, 400, str(err))
        except (psycopg2.Error, repository_exceptions.PostgresConnError, Exception) as err:
            return make_response_from_exception(err, 500, "Unexpected error happened on the server")

        return make_response(permissions, 200)
