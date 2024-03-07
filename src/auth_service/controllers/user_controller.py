import psycopg2
from flask import make_response, Response

from src.auth_service.services.user_service import UserService
from .controller import Controller
from src.auth_service.storage.entities.entities import User
from src.auth_service.storage.entities.serializers import UserSerializer


class UserController(Controller[User]):

    def __init__(self, request):
        self.data = request.json
        self.service = UserService()
        self.serializer = UserSerializer()

    def get(self, id_: int) -> Response:
        try:
            response = self.service.get(id_)
        except psycopg2.DataError as err:
            return make_response(str(err), 404)

        return make_response(self.serializer.deserialize(response), 200)

    def get_all(self) -> Response:
        try:
            responses = self.service.get_all()
        except psycopg2.DataError as err:
            return make_response(str(err), 404)

        return make_response([UserSerializer.deserialize(response) for response in responses], 200)

    def create(self) -> Response:
        try:
            self._create_data_check()
        except KeyError as err:
            return make_response(str(err), 400)

        user = UserSerializer.serialize(self.data)
        response = self.service.create(user)

        return make_response("200") if response else make_response("404", 404)

    def create_admin(self) -> Response:
        try:
            self._create_data_check()
        except KeyError as err:
            return make_response(str(err), 400)

        admin = UserSerializer.serialize(self.data)
        response = self.service.create(admin)

        return make_response("200") if response else make_response("404", 404)

    def _create_data_check(self):
        desired_keys = ['email', 'password']

        for key in desired_keys:
            if not self.data.get(key):
                raise KeyError(f"400: {key} is not provided")

