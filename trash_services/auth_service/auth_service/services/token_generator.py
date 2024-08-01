from flask import current_app

from datetime import datetime, timezone, timedelta
import jwt

class TokenGenerator:
    def __init__(self):
        self.algorithm = "HS256"

    def generate_access(self, id_: str, email: str, role: str) -> str:
        payload = self._generate_access_payload(id_, email, role)
        access_token = jwt.encode(payload=payload, algorithm=self.algorithm, key=current_app.secret_key)
        return access_token

    def generate_refresh(self, id_: str) -> str:
        payload = self._generate_refresh_payload(id_)
        refresh_token = jwt.encode(payload=payload, algorithm=self.algorithm, key=current_app.secret_key)
        return refresh_token

    @staticmethod
    def _generate_access_payload(id_: str, email: str, role: str) -> dict:
        return {
            "id": id_,
            "email": email,
            "role": role,
            "exp": datetime.now(tz=timezone.utc) + timedelta(days=1),  # <- expiration time
            "iat": datetime.now(tz=timezone.utc)  # <- time of issuing
        }

    @staticmethod
    def _generate_refresh_payload(id_: str) -> dict:
        return {
            "id": id_,
            "exp": datetime.now(tz=timezone.utc) + timedelta(weeks=1),  # <- expiration time
            "iat": datetime.now(tz=timezone.utc)  # <- time of issuing
        }
