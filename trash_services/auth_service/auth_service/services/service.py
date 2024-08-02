import random

from typing import List

from auth_service.storage.entities.entities import User
from auth_service.storage.repositories.repository import AuthRepository
from auth_service.services.token_generator import TokenGenerator
from auth_service.services.password_hasher import PasswordHasher
from auth_service.validators.credentials_validator import CredentialsValidator
from auth_service.validators.token_validator import TokenValidator

from auth_service.exceptions.service_exceptions import PasswordDoesNotMatch
from auth_service.exceptions.repository_exceptions import DataNotFound


class AuthService:

    def __init__(self,
                 repository: AuthRepository,
                 token_generator: TokenGenerator,
                 token_validator: TokenValidator,
                 password_hasher: PasswordHasher,
                 credentials_validator: CredentialsValidator):

        self.repository = repository
        self.token_generator = token_generator
        self.token_validator = token_validator
        self.credentials_validator = credentials_validator
        self.password_hasher = password_hasher

    def authorize(self, email: str, password: str) -> dict:
        user = self.authenticate(email, password)
        access_token = self.token_generator.generate_access(str(user.id), user.email, user.role)
        refresh_token = self.token_generator.generate_refresh(str(user.id))

        return {"access": access_token,
                "refresh": refresh_token,
                "id": user.id}

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

        # email validation + normalization
        user.email = self.credentials_validator.validate_email(email=user.email)

        # password validation + hashing
        self.credentials_validator.validate_password(password=user.password)
        user.password = self.password_hasher.hash(plain_password=user.password)

        self.repository.create(user)

        return user

    def delete(self, id_: int):
        self.repository.delete(id_)

    def update(self, id_, user: User):
        if user.email is not None:
            self.credentials_validator.validate_email(user.email)

        if user.password is not None:
            self.credentials_validator.validate_password(user.password)

        self.repository.update(id_, user)

    def randomize_id(self, lower_bound: int, upper_bound: int) -> int:
        while True:
            id_ = random.randint(lower_bound, upper_bound)
            try:
                self.repository.get(False, id_=id_)
            except DataNotFound:
                return id_

    def refresh_access_token(self, refresh_token: str) -> dict:
        id_ = self.token_validator.decode(refresh_token)["id"]
        user = self.get(id_)

        new_access_token = self.token_generator.generate_access(str(user.id), user.email, user.role)

        return {"access": new_access_token}
