import psycopg2
from flask import make_response, Response, request

from .controller import Controller
from microservices.auth_service.storage.entities.entities import User
from microservices.auth_service.storage.entities.serializers import UserSerializer

# TODO: hide error descriptions from users


class UserController(Controller[User]):

    def __init__(self, service):
        self.service = service
        self.serializer = UserSerializer()

    def get(self, id_: int) -> Response:
        # requires authorization
        try:
            response = self.service.get(id_)
        except psycopg2.Error:
            return make_response("Unexpected error happened on the server", 500)

        return make_response(self.serializer.deserialize(response), 200)

    def get_all(self) -> Response:
        # requires authorization
        try:
            responses = self.service.get_all()
        except psycopg2.Error:
            return make_response("Unexpected error happened on the server", 500)

        return make_response([UserSerializer.deserialize(response) for response in responses], 200)

    def create(self) -> Response:
        try:
            self._forbidden_input_check(['id', 'role_id'], request.json)
            self._desired_input_check(['email', 'password'], request.json)
        except KeyError as err:
            return make_response(str(err), 400)

        user = UserSerializer.serialize(request.json)

        try:
            if user == "create":
                self.service.create(user)
        except psycopg2.Error:
            return make_response("Unexpected error happened on the server", 500)

        return make_response("200")

    def create_admin(self) -> Response:
        try:
            self._forbidden_input_check(['id', 'role_id'], request.json)
            self._desired_input_check(['email', 'password'], request.json)
        except KeyError as err:
            return make_response(str(err), 400)

        admin = UserSerializer.serialize(request.json)

        try:
            self.service.create_admin(admin)
        except psycopg2.Error:
            return make_response("Unexpected error happened on the server", 500)

        return make_response("200")

    def delete(self, id_) -> Response:
        # requires authorization
        try:
            self.service.delete(id_)
        except psycopg2.Error:
            return make_response("Unexpected error happened on the server", 500)

        return make_response("200")

    def update(self, id_) -> Response:
        # requires authorization
        try:
            self._forbidden_input_check(['id', 'role_id'], request.json)
        except KeyError as err:
            return make_response(str(err), 400)

        user = UserSerializer.serialize(request.json)

        try:
            self.service.update(id_, user)
        except psycopg2.Error:
            return make_response("Unexpected error happened on the server", 500)

        return make_response("200")

    @staticmethod
    def _desired_input_check(desired_keys, request_json):
        # if called - checks that each "desired key" is passed in the request

        for key in desired_keys:
            if not request_json.get(key):
                raise KeyError(f"Desired key: \"{key}\" is not provided")

    @staticmethod
    def _forbidden_input_check(forbidden_keys, request_json):
        # if called - checks that no "forbidden key" is passed in the request

        for key in forbidden_keys:
            if request_json.get(key):
                raise KeyError(f"Forbidden key: \"{key}\" is provided")

    @staticmethod
    def _get_url_subdomain_by_index(index):
        return request.url_rule.rule.split('/')[index]
