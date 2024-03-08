import psycopg2
from flask import make_response, Response, g

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
        # requires authorization
        try:
            response = self.service.get(id_)

        except psycopg2.DataError as err:
            g.logger.error(f"{type(err).__name__}: {str(err)}")
            return make_response(str(err), 404)

        except Exception as err:
            g.logger.error(f"{type(err).__name__}: {str(err)}")
            return make_response(str(err), 400)

        return make_response(self.serializer.deserialize(response), 200)

    def get_all(self) -> Response:
        # requires authorization
        try:
            responses = self.service.get_all()

        except psycopg2.DataError as err:
            g.logger.error(f"{type(err).__name__}: {str(err)}")
            return make_response(str(err), 404)

        except Exception as err:
            g.logger.error(f"{type(err).__name__}: {str(err)}")
            return make_response(str(err), 400)

        return make_response([UserSerializer.deserialize(response) for response in responses], 200)

    def create(self) -> Response:
        try:
            self._creation_input_check()
            user = UserSerializer.serialize(self.data)
            self.service.create(user)

        except TypeError as err:
            g.logger.error(f"{type(err).__name__}: {str(err)}")
            return make_response("Bad input data", 400)

        except KeyError as err:
            g.logger.error(f"{type(err).__name__}: {str(err)}")
            return make_response(str(err), 400)

        except Exception as err:
            g.logger.error(f"{type(err).__name__}: {str(err)}")
            return make_response(str(err), 400)

        return make_response("200")

    def create_admin(self) -> Response:
        try:
            self._creation_input_check()
            admin = UserSerializer.serialize(self.data)
            self.service.create_admin(admin)

        except TypeError as err:
            g.logger.error(f"{type(err).__name__}: {str(err)}")
            return make_response("Bad input data", 400)

        except KeyError as err:
            g.logger.error(f"{type(err).__name__}: {str(err)}")
            return make_response(str(err), 400)

        except Exception as err:
            g.logger.error(f"{type(err).__name__}: {str(err)}")
            return make_response(str(err), 400)

        return make_response("200")

    def delete(self, id_) -> Response:
        # requires authorization
        try:
            self.service.delete(id_)

        except Exception as err:
            g.logger.error(f"{type(err).__name__}: {str(err)}")
            return make_response(str(err), 400)

        return make_response("200")

    def update(self, id_) -> Response:
        # requires authorization
        try:
            user = UserSerializer.serialize(self.data)
            self.service.update(id_, user)

        except TypeError as err:
            g.logger.error(f"{type(err).__name__}: {str(err)}")
            return make_response("Bad input data", 400)

        except Exception as err:
            g.logger.error(f"{type(err).__name__}: {str(err)}")
            return make_response(str(err), 400)

        return make_response("200")

    def _creation_input_check(self):
        desired_keys = ['email', 'password']

        for key in desired_keys:
            if not self.data.get(key):
                raise KeyError(f"400: {key} is not provided")
