import random

from auth_service.storage.entities.entities import User
from auth_service.storage.repositories.auth_repository import Repository
from auth_service.services.handlers import TokenHandler, PasswordHandler, EmailHandler

from auth_service.exceptions import service_exceptions, repository_exceptions


class Service:

    def __init__(self, repo: Repository):
        self.repo = repo

    def authorize(self, email: str, password: str) -> dict:
        user = self.authenticate(email, password)
        role = self.get_user_role(user.id)
        permissions = self.get_user_permissions(user.id)

        token_handler = TokenHandler()
        access_token = token_handler.generate_access(user.id, user.email, role, permissions)
        refresh_token = token_handler.generate_refresh(user.id)

        return {"access": access_token,
                "refresh": refresh_token}

    def authenticate(self, email, password) -> User:
        user = self.get_by_email(email)
        if user.password != PasswordHandler().hash(password):
            raise (service_exceptions.
                   PasswordDoesNotMatchError("Password doesnt match the stored one"))
        return user

    def refresh(self, refresh_token: str) -> dict:
        token_handler = TokenHandler()

        id_ = token_handler.decode(refresh_token)["id"]
        user = self.get(id_)

        role = self.get_user_role(id_)
        permissions = self.get_user_permissions(id_)

        token_handler = TokenHandler()
        new_access_token = token_handler.generate_access(user.id, user.email, role, permissions)

        return {"access": new_access_token}

    def get(self, id_: int, secure: bool = True) -> User:
        # "secure" parameter removes password from response body
        user = self.repo.get(id_, secure)
        return user

    def get_by_email(self, email: str) -> User:
        user = self.repo.get_by_email(email)
        return user

    def get_all(self, secure: bool) -> list[User]:
        # "secure" parameter removes passwords from response body
        users = self.repo.get_all(secure)
        return users

    def create(self, user: User, role_id: int) -> bool:
        user.id = self.randomize_id(1, 2 ** 31 - 1)
        user.role_id = role_id

        # email validation + normalization
        user.email = EmailHandler.validate(user.email)

        password_handler = PasswordHandler()
        # password validation + hashing
        password_handler.validate(user.password)
        user.password = password_handler.hash(user.password)

        return self.repo.create(user)

    def delete(self, id_: int) -> bool:
        return self.repo.delete(id_)

    def update(self, id_, user: User) -> bool:
        return self.repo.update(id_, user)

    def get_user_role(self, id_: int) -> int:
        return self.repo.get_role(id_)

    def get_user_permissions(self, id_) -> list[str]:
        return self.repo.get_permissions(id_)

    def randomize_id(self, lower_bound: int, upper_bound: int) -> int:
        while True:
            id_ = random.randint(lower_bound, upper_bound)
            try:
                self.get(id_, False)
            except repository_exceptions.UserNotFoundError:
                return id_
