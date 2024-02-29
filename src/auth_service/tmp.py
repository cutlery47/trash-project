from src.auth_service.storage.entities.entities import User
from src.auth_service.storage.entities.serializers import UserSerializer

data = {
    'id': 20,
    'email': "23123",
    'role_id': 10,
    'password': 'asfasf'
}

user = UserSerializer.serialize(data)
dat_2 = UserSerializer.deserialize(user)
print(dat_2)

