import random

from microservices.auth_service.storage.entities.entities import User
from microservices.auth_service.storage.repositories.auth_user_repository import UserRepository
from microservices.auth_service.services.token_handler import TokenHandler

from microservices.auth_service.exceptions import repository_exceptions
from microservices.auth_service.exceptions import service_exceptions

# TODO: implement password hashing
# TODO: implement JWT


class UserService:

    def __init__(self, repo: UserRepository):
        self.repo = repo

    def login(self, email, password):
        user = self.authenticate(email, password)

        role = self.get_user_role(user.id)
        permissions = self.get_user_permissions(user.id)

        token_handler = TokenHandler()
        access_token = token_handler.generate_access(user.id, user.email, role, permissions)
        refresh_token = token_handler.generate_refresh(user.id)

        return [access_token, refresh_token]

    def refresh(self, id_):
        pass

    def get(self, id_: int, secure: bool = True):
        # "secure" parameter removes password from response body
        user = self.repo.get(id_, secure)
        return user

    def get_by_email(self, email: str):
        user = self.repo.get_by_email(email)
        return user

    def get_all(self, secure: bool):
        # "secure" parameter removes passwords from response body
        users = self.repo.get_all(secure)
        return users

    def create(self, user: User):
        user.id = self.randomize_id(1, 2 ** 31 - 1)
        user.role_id = 0
        return self.repo.create(user)

    def create_admin(self, admin: User):
        admin.id = self.randomize_id(1, 2 ** 31 - 1)
        admin.role_id = 1
        return self.repo.create(admin)

    def delete(self, id_):
        return self.repo.delete(id_)

    def update(self, id_, user: User):
        return self.repo.update(id_, user)

    def get_user_role(self, id_):
        return self.repo.get_role(id_)

    def get_user_permissions(self, id_):
        return self.repo.get_permissions(id_)

    def authenticate(self, email, password):
        user = self.get_by_email(email)
        if user.password != password:
            raise (service_exceptions.
                   PasswordDoNotMatchError("Password doesnt match the stored one"))
        return user

    def randomize_id(self, lower_bound: int, upper_bound: int):
        while True:
            id_ = random.randint(lower_bound, upper_bound)
            try:
                self.get(id_, False)
            except repository_exceptions.UserNotFoundError:
                return id_
