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
        response = self.service.get(id_)
        if response != "None":
            return make_response(self.serializer.deserialize(response), 200)
        else:
            return make_response(response, 404)

    def get_all(self) -> Response:
        responses = self.service.get_all()
        if responses != "None":
            return make_response([self.serializer.deserialize(response) for response in responses], 2)
        else:
            return make_response(responses, 404)

    def create(self) -> Response:
        self._create_data_check()
        user = UserSerializer.serialize(self.data)
        response = self.service.create(user)
        # temporary
        return make_response("200") if response else make_response("404", 404)

    def create_admin(self) -> Response:
        self._create_data_check()
        admin = UserSerializer.serialize(self.data)
        response = self.service.create(admin)
        # temporary
        return make_response("200") if response else make_response("404", 404)

    def _create_data_check(self):
        desired_keys = ['email', 'password']

        for key in desired_keys:
            if not self.data.get(key):
                raise KeyError(f"{key} is not provided")

