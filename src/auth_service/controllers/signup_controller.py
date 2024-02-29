from builtins import classmethod
from flask import Request

from src.auth_service.services.services import SignUpService
from controller import Controller



class SignUpController(Controller):
    desired_keys = ['id', 'role', 'email', 'password']
    data = {}

    @classmethod
    def __init__(cls, request: Request):
        cls.request = request

    @classmethod
    def handle(cls):
        cls._integrity_check()
        return SignUpService(cls.data)

    @classmethod
    def _integrity_check(cls):
        for key in cls.desired_keys:
            if cls.request.form.get(key):
                cls.data[key] = cls.request.form[key]
            else:
                raise KeyError(f"{key} is not provided")


