import random

from fastapi import Response

from typing import List

from src.storage.entities.entities import User
from src.storage.repositories.repository import AuthRepository
from src.service.token_generator import TokenGenerator
from src.service.password_hasher import PasswordHasher

from src.exceptions.service_exceptions import PasswordDoesNotMatch
from src.exceptions.repository_exceptions import DataNotFound


class AuthService:

    def __init__(self,
                 repository: AuthRepository,
                 token_generator: TokenGenerator,
                 password_hasher: PasswordHasher):

        self.repository = repository
        self.token_generator = token_generator
        self.password_hasher = password_hasher

    def authorize(self, email: str, password: str, response: Response):
        user = self.authenticate(email, password)
        access_token = self.token_generator.generate_access(str(user.id), user.email, user.role)
        refresh_token = self.token_generator.generate_refresh(str(user.id))

        response.set_cookie("access", access_token)
        response.set_cookie("refresh", refresh_token)

    def authenticate(self, email: str, password: str) -> User:
        user = self.get(email=email, is_secure=False)
        if user.password != self.password_hasher.hash(password):
            raise PasswordDoesNotMatch("Password doesnt match the stored one")

        return user

    # "is_secure" parameter removes password from response body

    def get(self, id_: int = None, email: str = None, is_secure: bool = True) -> User | List:
        if id_ is not None:
            # get user by id
            return self.repository.get(is_secure=is_secure, id_=id_)
        elif email is not None:
            # get user by email
            return self.repository.get(is_secure=is_secure, email=email)
        else:
            # get all the users
            return self.repository.get_all(is_secure=is_secure)

    def create(self, user: User) -> User:
        user.id = self.randomize_id(1, 2 ** 31 - 1)
        user.password = self.password_hasher.hash(plain_password=user.password)
        self.repository.create(user)
        return user

    def delete(self, id_: int):
        self.repository.delete(id_)

    def update(self, id_, user: User):
        self.repository.update(id_, user)

    def randomize_id(self, lower_bound: int, upper_bound: int) -> int:
        while True:
            id_ = random.randint(lower_bound, upper_bound)
            if not self.repository.exists(id_):
                return id_

    def refresh_access_token(self, refresh_token: dict, response: Response) -> Response:
        id_ = refresh_token.get("id")
        user = self.get(id_)
        new_access_token = self.token_generator.generate_access(str(user.id), user.email, user.role)

        response.set_cookie("access", new_access_token)

        return response

