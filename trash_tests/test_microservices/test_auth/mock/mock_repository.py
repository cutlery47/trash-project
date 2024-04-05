from auth_service.interfaces.auth_repository_interface import AuthRepositoryInterface
from auth_service.storage.entities.entities import User
from auth_service.storage.entities.serializers import UserSerializer

from auth_service.exceptions import repository_exceptions


class MockAuthRepository(AuthRepositoryInterface):
    def __init__(self):
        self.users = {}
        self.roles = {
            0: "user",
            1: "admin"
        }
        self.permissions = {
            0: 'GET SINGLE USER DATA',
            1: 'GET MULTIPLE USERS DATA',
            2: 'UPDATE ANY USER DATA',
            3: 'DELETE ANY USER',
            4: 'GET ANY USER ROLE',
            5: 'GET ANY USER PERMISSION',
            6: 'CREATE ADMIN',
            7: 'PROMOTE TO ADMIN'
        }
        self.role_permissions = {
            0: [0, 1],
            1: [0, 1, 2, 3, 4, 5, 6, 7]
        }

    def get(self, secure: bool, id_: int = None, email: str = None) -> User:
        user = None
        if id_ is not None:
            user = self.users.get(id_)
        else:
            for user_data in self.users.values():
                if user_data["email"] == email:
                    user = user_data
                    break

        if not user:
            raise repository_exceptions.UserNotFoundError("User was not found")

        return User(**user)

    def get_all(self, secure: bool) -> list[User]:
        return [User(self.users[key]) for key in self.users.keys()]

    def create(self, user_data: User) -> bool:
        for val in self.users.values():
            if val["email"] == user_data.email:
                raise repository_exceptions.UniqueConstraintError("User with this email already exists")

        self.users[user_data.id] = UserSerializer.serialize(user_data)
        print(self.users)
        return True

    def delete(self, id_: int) -> bool:
        user = self.users.get(id_)
        if not user:
            raise repository_exceptions.UserNotFoundError("User was not found")

        self.users.pop(id_)
        return True

    def update(self, id_: int, user_data: User) -> bool:
        user = self.users.get(id_)
        if not user:
            raise repository_exceptions.UserNotFoundError("User was not found")

        self.users[id_] = UserSerializer.serialize(user_data)
        return True

    def get_role(self, id_: int) -> int:
        user = self.users.get(id_)
        if not user:
            raise repository_exceptions.UserNotFoundError("User was not found")

        user = User(**self.users.get(id_))
        return user.role_id


    def get_permissions(self, id_: int) -> list[str]:
        user = self.users.get(id_)
        if not user:
            raise repository_exceptions.UserNotFoundError("User was not found")

        user = User(**self.users.get(id_))
        role_id = user.role_id
        permissions_ids = self.role_permissions.get(role_id)

        permissions = []
        for perm_id in permissions_ids:
            permissions.append(self.permissions[perm_id])

        return permissions














