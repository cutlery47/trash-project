from datetime import timezone, datetime, timedelta
import jwt

from auth_service.exceptions import token_exceptions


class TokenHandler:
    def __init__(self):
        self.secret = open("auth_service/config/app/jwt_secret.txt").read()
        self.algorithm = "HS256"

    def generate_access(self, id_, email, role, permissions) -> str:
        payload = self._generate_access_payload(id_, email, role, permissions)

        access_token = jwt.encode(payload=payload, algorithm=self.algorithm, key=self.secret)
        return access_token

    def generate_refresh(self, id_) -> str:
        payload = self._generate_refresh_payload(id_)

        refresh_token = jwt.encode(payload=payload, algorithm=self.algorithm, key=self.secret)
        return refresh_token

    def verify(self, token):
        try:
            decoded = jwt.decode(token, algorithms=self.algorithm, key=self.secret)

        except jwt.PyJWTError as err:
            raise token_exceptions.TokenIsInvalid(str(err))

        return decoded

    def decode(self, token) -> dict:
        # simply decodes all the data without any verification
        return jwt.decode(token, algorithms=self.algorithm, key=self.secret, options={"verify_signature": False})


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
    def _generate_refresh_payload(id_) -> dict:
        return {
            "id": id_,
            "exp": datetime.now(tz=timezone.utc) + timedelta(weeks=1),
            "iat": datetime.now(tz=timezone.utc)
        }