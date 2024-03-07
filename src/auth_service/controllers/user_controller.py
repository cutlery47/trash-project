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

