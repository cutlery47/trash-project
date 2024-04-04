import random

from auth_service.storage.entities.entities import User
from auth_service.storage.repositories.auth_repository import AuthRepository
from auth_service.services.handlers import TokenHandler, PasswordHandler, EmailHandler

from auth_service.exceptions import service_exceptions, repository_exceptions


class AuthService:

    def __init__(self, repository: AuthRepository, token_handler: TokenHandler,
                 password_handler: PasswordHandler, email_handler: EmailHandler):
        self.repository = repository
        self.token_handler = token_handler
        self.password_handler = password_handler
        self.email_handler = email_handler

    def authorize(self, email: str, password: str) -> dict:
        user = self.authenticate(email, password)
        role = self.get_user_role(user.id)
        permissions = self.get_user_permissions(user.id)

        access_token = self.token_handler.generate_access(user.id, user.email, role, permissions)
        refresh_token = self.token_handler.generate_refresh(user.id)
        return {"access": access_token,
                "refresh": refresh_token}

    def authenticate(self, email, password) -> User:
        user = self.get_by_email(email, secure=False)
        if user.password != self.password_handler.hash(password):
            raise (service_exceptions.
                   PasswordDoesNotMatchError("Password doesnt match the stored one"))
        return user

    def refresh(self, refresh_token: str) -> dict:
        id_ = self.token_handler.decode(refresh_token)["id"]
        user = self.get(id_)
        role = self.get_user_role(id_)
        permissions = self.get_user_permissions(id_)

        new_access_token = self.token_handler.generate_access(user.id, user.email, role, permissions)
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

    def create(self, user: User, role_id: int) -> bool:
        user.id = self.randomize_id(1, 2 ** 31 - 1)
        user.role_id = role_id

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

    def get_user_role(self, id_: int) -> int:
        return self.repository.get_role(id_)

    def get_user_permissions(self, id_) -> list[str]:
        return self.repository.get_permissions(id_)

    def randomize_id(self, lower_bound: int, upper_bound: int) -> int:
        while True:
            id_ = random.randint(lower_bound, upper_bound)
            try:
                self.get(id_, False)
            except repository_exceptions.UserNotFoundError:
                return id_
