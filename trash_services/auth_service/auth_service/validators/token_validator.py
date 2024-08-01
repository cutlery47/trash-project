from flask import request, current_app

import jwt

from auth_service.exceptions.validation_exceptions import (RequiredFieldsNotProvided,
                                                           NotAllowedToAccessResource,
                                                           TokenIsInvalid,
                                                           EmailIsInvalid)

class TokenValidator:

    algorithm = "HS256"

    def decode(self, jwt_: str, validate: bool = True) -> dict:
        try:
            decoded = jwt.decode(jwt=jwt_,
                                 algorithms=self.algorithm,
                                 key=current_app.secret_key,
                                 options={"verify_signature": validate})
        except jwt.PyJWTError as err:
            raise TokenIsInvalid(f"Provided token is invalid: {str(err)}")

        return decoded

    def get_access_token(self, validate: bool) -> dict:

        access_token = request.cookies.get("access")
        if not access_token:
            raise RequiredFieldsNotProvided(description="Access token is required")

        return self.decode(jwt_=access_token, validate=validate)

    def get_refresh_token(self, validate: bool) -> dict:

        refresh_token = request.cookies.get("refresh")
        if not refresh_token:
            raise RequiredFieldsNotProvided(description=f"Refresh token is required")

        return self.decode(jwt_=refresh_token, validate=validate)

    def validate_admin(self):

        decoded = self.get_access_token(validate=False)

        role = decoded.get("role")
        if role != "admin":
            #raise EmailIsInvalid("123123123")
            raise NotAllowedToAccessResource("Admin rights are required to access this resource")

    def validate_id_access(self):

        decoded = self.get_access_token(validate=False)

        token_id = decoded.get('id')
        requested_id = request.url.split('/')[-1]

        if token_id != requested_id:
            raise NotAllowedToAccessResource("You can't access data by the provided id")