import psycopg2
from flask import make_response, Response, request, current_app

from microservices.auth_service.services.auth_user_service import UserService
from microservices.auth_service.storage.entities.serializers import UserSerializer

from microservices.auth_service.exceptions import repository_exceptions, controller_exceptions, service_exceptions

# TODO: implement JWT verification


class UserController:

    def __init__(self, service: UserService):
        self.service = service
        self.serializer = UserSerializer()

    def register(self):
        # wrapper over default user creation
        return self._create()

    def register_admin(self):
        # wrapper over default admin creation
        return self._create_admin()

    def login(self):
        try:
            self._desired_input_check(['email', 'password'], request.json)

        except (controller_exceptions.DesiredFieldsNotProvidedError,
                controller_exceptions.ForbiddenFieldsProvidedError) as err:
            return self._make_response_from_exception(err, 400, str(err))

        email = request.json.get('email')
        password = request.json.get('password')

        try:
            result = self.service.login(email, password)

        except (service_exceptions.PasswordDoNotMatchError,
                repository_exceptions.UserNotFoundError) as err:
            return self._make_response_from_exception(err, 400, "Password or email are invalid")

        return make_response("Authorized")

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

    def _create(self) -> Response:
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

        return make_response(str(user_id))

    def _create_admin(self) -> Response:
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

        return make_response(str(user_id))

    def delete(self, id_) -> Response:
        # requires authorization
        try:
            self.service.delete(id_)

        except repository_exceptions.UserNotFoundError as err:
            return self._make_response_from_exception(err, 400, str(err))

        except (psycopg2.Error, repository_exceptions.PostgresConnError, Exception) as err:
            return self._make_response_from_exception(err, 500, "Unexpected error happened on the server")

        return make_response("200")

    def update(self, id_) -> Response:
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

        return make_response("200")

    def get_user_role(self, id_) -> Response:
        try:
            role = self.service.get_user_role(id_)

        except repository_exceptions.RoleNotFound as err:
            return self._make_response_from_exception(err, 400, str(err))

        except (psycopg2.Error, repository_exceptions.PostgresConnError, Exception) as err:
            return self._make_response_from_exception(err, 500, "Unexpected error happened on the server")

        return make_response(role)

    def get_user_permissions(self, id_) -> Response:
        try:
            role = self.service.get_user_permissions(id_)

        except repository_exceptions.PermissionsNotFoundError as err:
            return self._make_response_from_exception(err, 400, str(err))

        except (psycopg2.Error, repository_exceptions.PostgresConnError, Exception) as err:
            return self._make_response_from_exception(err, 500, "Unexpected error happened on the server")

        return make_response(role)

    @staticmethod
    def _make_response_from_exception(err: Exception, status: int, response: str) -> Response:
        current_app.logger.error(f"{type(err).__name__}: {str(err)}")
        return make_response(response, status)

    @staticmethod
    def _desired_input_check(desired_keys, request_json):
        # if called - checks that each "desired key" is passed in the request

        for key in desired_keys:
            if not request_json.get(key):
                raise controller_exceptions.DesiredFieldsNotProvidedError(f"Desired key: \"{key}\" is not provided")

    @staticmethod
    def _forbidden_input_check(forbidden_keys, request_json):
        # if called - checks that no "forbidden key" is passed in the request

        for key in forbidden_keys:
            if request_json.get(key):
                raise controller_exceptions.ForbiddenFieldsProvidedError(f"Forbidden key: \"{key}\" is provided")

    @staticmethod
    def _get_url_subdomain_by_index(index):
        return request.url_rule.rule.split('/')[index]
