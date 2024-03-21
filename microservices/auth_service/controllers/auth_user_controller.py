import psycopg2
from flask import make_response, Response, request, current_app

from microservices.auth_service.services.auth_user_service import UserService
from microservices.auth_service.storage.entities.serializers import UserSerializer

from microservices.auth_service.exceptions import repository_exceptions, controller_exceptions, service_exceptions

# TODO: implement JWT verification
# TODO: stash all the data checks into decorators


class UserController:

    def __init__(self, service: UserService):
        self.service = service
        self.serializer = UserSerializer()

    # wrapper over default user creation
    def register(self) -> Response:
        return self.register()

    # wrapper over default admin creation
    def register_admin(self) -> Response:
        return self.register_admin()

    def authorize(self) -> Response:
        try:
            self._desired_input_check(['email', 'password'], request.json)

        except (controller_exceptions.DesiredFieldsNotProvidedError,
                controller_exceptions.ForbiddenFieldsProvidedError) as err:
            return self._make_response_from_exception(err, 400, str(err))

        email = request.json['email']
        password = request.json['password']

        try:
            result = self.service.authorize(email, password)

        except (service_exceptions.PasswordDoesNotMatchError,
                repository_exceptions.UserNotFoundError) as err:
            return self._make_response_from_exception(err, 400, "Password or email are invalid")

        except (psycopg2.Error, repository_exceptions.PostgresConnError, Exception) as err:
            return self._make_response_from_exception(err, 500, "Unexpected error happened on the server")

        return make_response(result, 200)

    def refresh(self) -> Response:
        try:
            self._desired_input_check(["id"], request.json)

        except controller_exceptions.DesiredFieldsNotProvidedError as err:
            return self._make_response_from_exception(err, 400, str(err))

        id_ = request.json.get("id")

        try:
            refresh_token = self.service.refresh(id_)

        except (psycopg2.Error, repository_exceptions.PostgresConnError, Exception) as err:
            return self._make_response_from_exception(err, 500, "Unexpected error happened on the server")

        return make_response(refresh_token, 200)

    def get(self, id_: int) -> Response:
        # requires authorization
        try:
            response = self.service.get(id_, True)

        except repository_exceptions.UserNotFoundError as err:
            return self._make_response_from_exception(err, 400, str(err))

        except (psycopg2.Error, repository_exceptions.PostgresConnError, Exception) as err:
            return self._make_response_from_exception(err, 500, "Unexpected error happened on the server")

        return make_response(self.serializer.serialize(response), 200)

    def get_all(self) -> Response:
        # requires authorization
        try:
            responses = self.service.get_all(True)

        except (psycopg2.Error, repository_exceptions.PostgresConnError, Exception) as err:
            return self._make_response_from_exception(err, 500, "Unexpected error happened on the server")

        return make_response([UserSerializer.serialize(response) for response in responses], 200)

    def create(self) -> Response:
        try:
            self._forbidden_input_check(['id', 'role_id'], request.json)
            self._desired_input_check(['email', 'password'], request.json)

        except (controller_exceptions.DesiredFieldsNotProvidedError,
                controller_exceptions.ForbiddenFieldsProvidedError) as err:
            return self._make_response_from_exception(err, 400, str(err))

        user = UserSerializer.deserialize(request.json)

        try:
            user_id = self.service.create(user)

        except repository_exceptions.UniqueConstraintError as err:
            return self._make_response_from_exception(err, 400, str(err))

        except (psycopg2.Error, repository_exceptions.PostgresConnError, Exception) as err:
            return self._make_response_from_exception(err, 500, "Unexpected error happened on the server")

        return make_response(str(user_id), 200)

    def create_admin(self) -> Response:
        try:
            self._forbidden_input_check(['id', 'role_id'], request.json)
            self._desired_input_check(['email', 'password'], request.json)

        except (controller_exceptions.DesiredFieldsNotProvidedError,
                controller_exceptions.ForbiddenFieldsProvidedError) as err:
            return self._make_response_from_exception(err, 400, str(err))

        admin = UserSerializer.deserialize(request.json)

        try:
            user_id = self.service.create_admin(admin)

        except repository_exceptions.UniqueConstraintError as err:
            return self._make_response_from_exception(err, 400, str(err))

        except (psycopg2.Error, repository_exceptions.PostgresConnError, Exception) as err:
            return self._make_response_from_exception(err, 500, "Unexpected error happened on the server")

        return make_response(str(user_id), 200)

    def delete(self, id_: int) -> Response:
        # requires authorization
        try:
            self.service.delete(id_)

        except repository_exceptions.UserNotFoundError as err:
            return self._make_response_from_exception(err, 400, str(err))

        except (psycopg2.Error, repository_exceptions.PostgresConnError, Exception) as err:
            return self._make_response_from_exception(err, 500, "Unexpected error happened on the server")

        return make_response("200", 200)

    def update(self, id_: int) -> Response:
        # requires authorization
        try:
            self._forbidden_input_check(['id', 'role_id'], request.json)

        except controller_exceptions.ForbiddenFieldsProvidedError as err:
            return self._make_response_from_exception(err, 400, str(err))

        user = UserSerializer.deserialize(request.json)

        try:
            self.service.update(id_, user)

        except repository_exceptions.UserNotFoundError as err:
            return self._make_response_from_exception(err, 400, str(err))

        except (psycopg2.Error, repository_exceptions.PostgresConnError, Exception) as err:
            return self._make_response_from_exception(err, 500, "Unexpected error happened on the server")

        return make_response("200", 200)

    def get_user_role(self, id_: int) -> Response:
        try:
            role = self.service.get_user_role(id_)

        except repository_exceptions.RoleNotFoundError as err:
            return self._make_response_from_exception(err, 400, str(err))

        except (psycopg2.Error, repository_exceptions.PostgresConnError, Exception) as err:
            return self._make_response_from_exception(err, 500, "Unexpected error happened on the server")

        return make_response(role, 200)

    def get_user_permissions(self, id_: int) -> Response:
        try:
            role = self.service.get_user_permissions(id_)

        except repository_exceptions.PermissionsNotFoundError as err:
            return self._make_response_from_exception(err, 400, str(err))

        except (psycopg2.Error, repository_exceptions.PostgresConnError, Exception) as err:
            return self._make_response_from_exception(err, 500, "Unexpected error happened on the server")

        return make_response(role, 200)

    @staticmethod
    def _make_response_from_exception(err: Exception, status: int, response: str) -> Response:
        current_app.logger.error(f"{type(err).__name__}: {str(err)}")
        return make_response(response, status)

    @staticmethod
    def _desired_input_check(desired_keys: list, request_json: dict) -> bool:
        # if called - checks that each "desired key" is passed in the request

        for key in desired_keys:
            if not request_json.get(key):
                raise controller_exceptions.DesiredFieldsNotProvidedError(f"Desired key: \"{key}\" is not provided")

        return True

    @staticmethod
    def _forbidden_input_check(forbidden_keys: list, request_json: dict) -> bool:
        # if called - checks that no "forbidden key" is passed in the request

        for key in forbidden_keys:
            if request_json.get(key):
                raise controller_exceptions.ForbiddenFieldsProvidedError(f"Forbidden key: \"{key}\" is provided")

        return True

    @staticmethod
    def _get_url_subdomain_by_index(index: int) -> str:
        return request.url_rule.rule.split('/')[index]
