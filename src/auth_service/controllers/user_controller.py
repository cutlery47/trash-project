from src.auth_service.services.user_service import UserService
from .controller import Controller
from src.auth_service.storage.entities.entities import User
from src.auth_service.storage.entities.serializers import UserSerializer


class UserController(Controller[User]):

    def __init__(self, request):
        self.data = request.json
        self.service = UserService()
        self.serializer = UserSerializer()

    def handle_get(self, id_: int):
        response = self.service.get(id_)
        return self.serializer.deserialize(response)

    def handle_get_all(self):
        responses = self.service.get_all()
        return [self.serializer.deserialize(response) for response in responses]

    def _integrity_check(self):
        pass


# class SignUpController(Controller):
#     desired_keys = ['id', 'role_id', 'email', 'password']
#     data = {}
#
#     @classmethod
#     def __init__(cls, request: Request):
#         cls.request = request
#
#     @classmethod
#     def handle(cls):
#         cls._integrity_check()
#         return SignUpService.handle(cls.data)
#
#     @classmethod
#     def _integrity_check(cls):
#         for key in cls.desired_keys:
#             if cls.request.form.get(key):
#                 cls.data[key] = cls.request.form[key]
#             else:
#                 raise KeyError(f"{key} is not provided")


