from src.service.service import AuthService
from src.storage.entities.entities import User

from src.validators.token_validator import TokenValidator
from src.validators.input_validator import InputValidator
from src.validators.credentials_validator import CredentialsValidator

from fastapi import Request, Response

from typing import List

class AuthController:

    def __init__(self,
                 service: AuthService,
                 token_validator: TokenValidator,
                 input_validator: InputValidator,
                 credentials_validator: CredentialsValidator):
        self.service = service
        self.token_validator = token_validator
        self.input_validator = input_validator
        self.credentials_validator = credentials_validator

    def validate_access_token(self, request: Request) -> dict:
        return self.token_validator.get_or_validate_access_token(validate=True,
                                                                 request=request)

    def validate_admin(self, request: Request, token: dict = None):
        if token is None:
            token = self.token_validator.get_or_validate_access_token(validate=False,
                                                                      request=request)
        self.token_validator.validate_admin(token)

    def validate_access_to_id(self, request: Request, id_: int, token: dict = None,):
        if token is None:
            token = self.token_validator.get_or_validate_access_token(validate=False,
                                                                      request=request)
        self.token_validator.validate_id_access(token=token,
                                                id_=id_)

    def authorize(self, email: str, password: str, response: Response):
        self.service.authorize(email, password, response)

    def refresh(self, request: Request, response: Response):
        refresh_token = self.token_validator.get_or_validate_refresh_token(validate=True,
                                                                           request=request)
        self.service.refresh_access_token(refresh_token, response)

    def get(self, id_: int) -> dict:
        user = self.service.get(id_=id_, is_secure=True)
        return user.serialize()

    def get_all(self) -> List[dict]:
        users = self.service.get(is_secure=True)
        return [user.serialize() for user in users]

    def create(self, email: str, password: str, firstname: str, surname: str, role: str) -> dict:
        self.credentials_validator.validate_email(email)
        self.credentials_validator.validate_password(password)

        user = User(email=email,
                    password=password,
                    firstname=firstname,
                    surname=surname,
                    role=role)

        created_user = self.service.create(user)

        return created_user.serialize(is_secure=True)

    def delete(self, id_: int):
        self.service.delete(id_)

    def update(self, id_: int, email: str = None, password: str = None, firstname: str = None, surname: str = None):
        if email is not None:
            self.credentials_validator.validate_email(email)

        if password is not None:
            self.credentials_validator.validate_password(password)

        user = User(email=email,
                    password=password,
                    firstname=firstname,
                    surname=surname)

        self.service.update(id_, user)
