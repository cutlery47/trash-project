import random

from user_service.storage.entities.entities import User
from user_service.storage.repositories.repository import AuthRepository
from user_service.services.handlers import TokenHandler, PasswordHandler, EmailHandler

from user_service.exceptions import service_exceptions, repository_exceptions


class AuthService:

    def __init__(self, repository: AuthRepository, token_handler: TokenHandler,
                 password_handler: PasswordHandler, email_handler: EmailHandler):
        self.repository = repository
        self.token_handler = token_handler
        self.password_handler = password_handler
        self.email_handler = email_handler

    def authorize(self, email: str, password: str) -> dict:
        user = self.authenticate(email, password)

        access_token = self.token_handler.generate_access(user.id, user.email, user.role)
        refresh_token = self.token_handler.generate_refresh(user.id)

        return {"access": access_token,
                "refresh": refresh_token,
                "id": user.id}

    def authenticate(self, email, password) -> User:
        user = self.get_by_email(email, secure=False)
        print(f"authent: {user.id}")
        if user.password != self.password_handler.hash(password):
            raise (service_exceptions.
                   PasswordDoesNotMatchError("Password doesnt match the stored one"))
        return user

    def refresh(self, refresh_token: str) -> dict:
        id_ = self.token_handler.decode(refresh_token)["id"]
        user = self.get(id_)

        new_access_token = self.token_handler.generate_access(user.id, user.email, user.role)
        return {"access": new_access_token}

    def get(self, id_: int, secure: bool = True) -> User:
        # "secure" parameter removes password from response body
        user = self.repository.get(secure, id_=id_)
        return user

    def get_by_email(self, email: str, secure: bool = True) -> User:
        user = self.repository.get(secure, email=email)
        return user

    def get_all(self, secure: bool) -> list[User]:
        # "secure" parameter removes passwords from response body
        users = self.repository.get_all(secure)
        return users

    def create(self, user: User) -> bool:
        user.id = self.randomize_id(1, 2 ** 31 - 1)
        print(f"creation: {user.id}")

        # email validation + normalization
        user.email = self.email_handler.validate(user.email)

        # password validation + hashing
        self.password_handler.validate(user.password)
        user.password = self.password_handler.hash(user.password)

        return self.repository.create(user)

    def delete(self, id_: int) -> bool:
        return self.repository.delete(id_)

    def update(self, id_, user: User) -> bool:
        return self.repository.update(id_, user)

    def randomize_id(self, lower_bound: int, upper_bound: int) -> int:
        while True:
            id_ = random.randint(lower_bound, upper_bound)
            try:
                self.repository.get(False, id_=id_)
            except repository_exceptions.UserNotFoundError:
                return id_
