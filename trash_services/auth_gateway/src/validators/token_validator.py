import os

import jwt

from src.exceptions.validation_exceptions import (RequiredFieldsNotProvided,
                                                  NotAllowedToAccessResource,
                                                  TokenIsInvalid)

from fastapi.requests import Request

SECRET_KEY = os.getenv("SECRET_KEY", "SECRET_KEY")

class TokenValidator:

    algorithm = "HS256"

    def decode(self, raw_jwt_: str, validate: bool = True) -> dict:
        try:
            decoded = jwt.decode(jwt=raw_jwt_,
                                 algorithms=self.algorithm,
                                 options={"verify_signature": validate},
                                 key=SECRET_KEY)
        except jwt.PyJWTError as err:
            raise TokenIsInvalid(f"Provided token is invalid: {str(err)}")

        return decoded

    def get_or_validate_access_token(self, validate: bool, request: Request) -> dict:
        access_token = request.cookies.get("access")

        if not access_token:
            raise RequiredFieldsNotProvided("Access token is required")

        return self.decode(raw_jwt_=access_token, validate=validate)

    def get_or_validate_refresh_token(self, validate: bool, request: Request) -> dict:
        refresh_token = request.cookies.get("refresh")

        if not refresh_token:
            raise RequiredFieldsNotProvided(f"Refresh token is required")

        return self.decode(raw_jwt_=refresh_token, validate=validate)

    @staticmethod
    def validate_admin(token: dict):
        role = token.get("role")
        if role != "admin":
            raise NotAllowedToAccessResource("Admin rights are required to access this resource")

    @staticmethod
    def validate_id_access(token: dict, id_: int):
        token_id = token.get('id')
        requested_id = str(id_)

        if token_id != requested_id:
            raise NotAllowedToAccessResource("You can't access data by the provided id")