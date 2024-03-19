from datetime import timezone, datetime, timedelta
import jwt


class TokenHandler:
    def __init__(self):
        self.secret = open("microservices/auth_service/config/app/jwt_secret.txt").read()
        self.algorithm = "HS256"

    def generate_access(self, id_, email, roles, permissions):
        payload = self._generate_access_payload(id_, email, roles, permissions)

        access_token = jwt.encode(payload=payload, algorithm=self.algorithm, key=self.secret)
        return access_token

    def generate_refresh(self, id_):
        payload = self._generate_refresh_payload(id_)

        refresh_token = jwt.encode(payload=payload, algorithm=self.algorithm, key=self.secret)
        return refresh_token

    def decode(self, token):
        return jwt.decode(token, algorithms=self.algorithm, key=self.secret)

    @staticmethod
    def _generate_access_payload(id_, email, role, permissions) -> dict:
        return {
            "id": id_,
            "email": email,
            "role": role,
            "permissions": permissions,
            "exp": datetime.now(tz=timezone.utc) + timedelta(hours=1),  # <- expiration time
            "iat": datetime.now(tz=timezone.utc)  # <- time of issuing
        }

    @staticmethod
    def _generate_refresh_payload(id_):
        return {
            "id": id_,
            "exp": datetime.now(tz=timezone.utc) + timedelta(weeks=1),
            "iat": datetime.now(tz=timezone.utc)
        }