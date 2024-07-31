from flask import current_app, make_response, Response, request
import jwt

from auth_service.exceptions.validation_exceptions import (RequiredFieldsNotProvided,
                                                           NotAllowedToAccessResource,
                                                           ForbiddenFieldsAreProvided,
                                                           TokenIsInvalid,
                                                           AdminRoleRequired)

class InputValidator:

    @staticmethod
    def validate_required(required_fields, json):
        for field in required_fields:
            if not json.get(field):
                raise RequiredFieldsNotProvided(description=f"Desired field: \"{field}\" is not provided")

    @staticmethod
    def validate_forbidden(forbidden_fields, json):
        for field in forbidden_fields:
            if json.get(field):
                raise ForbiddenFieldsAreProvided(description=f"Forbidden field: \"{field}\" is provided")


class TokenValidator:

    algorithm = "HS256"

    def decode(self, jwt_: str, is_secure: bool = True) -> dict:
        try:
            decoded = jwt.decode(jwt=jwt_,
                                 algorithms=self.algorithm,
                                 key=current_app.secret_key,
                                 options={"verify_signature": is_secure})
        except jwt.PyJWTError as err:
            raise TokenIsInvalid(f"Provided token is invalid: {str(err)}")

        return decoded

    def validate_access(self) -> dict:

        access_token = request.cookies.get("access")
        if not access_token:
            raise RequiredFieldsNotProvided(description="Access token is required")

        return self.decode(jwt_=access_token, is_secure=True)

    def validate_refresh(self) -> dict:

        refresh_token = request.cookies.get("refresh")
        if not refresh_token:
            raise RequiredFieldsNotProvided(description=f"Refresh token is required")

        return self.decode(jwt_=refresh_token, is_secure=True)

    def validate_admin(self):

        decoded = self.validate_access()

        role = decoded.get("role")
        if role != "admin":
            raise NotAllowedToAccessResource("Admin rights are required to access this resource")

    def validate_id_access(self):

        decoded = self.validate_access()

        token_id = decoded.get('id')
        requested_id = request.url.split('/')[-1]

        if token_id != requested_id:
            raise NotAllowedToAccessResource("You can't access data by the provided id")
