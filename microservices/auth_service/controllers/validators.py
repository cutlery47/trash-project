from flask import current_app, make_response, Response

from microservices.auth_service.exceptions import controller_exceptions, token_exceptions
from microservices.auth_service.services.token_handler import TokenHandler


def make_response_from_exception(err: Exception, status: int, response: str) -> Response:
    current_app.logger.error(f"{type(err).__name__}: {str(err)}")
    return make_response(response, status)


class InputValidator:
    def validate_desired(self, desired_keys, json) -> bool or Response:
        # checks that each key is present in the request body
        try:
            self._desired_keys_provided(desired_keys, json)

        except (controller_exceptions.DesiredFieldsNotProvidedError,
                controller_exceptions.ForbiddenFieldsProvidedError) as err:
            return make_response_from_exception(err, 400, str(err))

        return True

    def validate_forbidden(self, forbidden_keys, json) -> bool or Response:
        # checks that no extra keys are present in the request body
        try:
            self._forbidden_keys_not_provided(forbidden_keys, json)

        except (controller_exceptions.DesiredFieldsNotProvidedError,
                controller_exceptions.ForbiddenFieldsProvidedError) as err:
            return make_response_from_exception(err, 400, str(err))

        return True

    @staticmethod
    def _desired_keys_provided(desired_keys: list, json: dict):
        for key in desired_keys:
            if not json.get(key):
                raise controller_exceptions.DesiredFieldsNotProvidedError(f"Desired key: \"{key}\" is not provided")

        return True

    @staticmethod
    def _forbidden_keys_not_provided(forbidden_keys: list, json: dict):
        for key in forbidden_keys:
            if json.get(key):
                raise controller_exceptions.ForbiddenFieldsProvidedError(f"Forbidden key: \"{key}\" is provided")

        return True


class TokenValidator:
    @staticmethod
    def validate_access(json) -> bool or Response:
        input_validator = InputValidator()
        input_validator_response = input_validator.validate_desired(desired_keys=['access'],
                                                                    json=json)

        if input_validator_response is not True:
            return input_validator_response

        access_token = json['access']
        token_handler = TokenHandler()

        try:
            token_handler.verify(access_token)

        except token_exceptions.TokenIsInvalid as err:
            return make_response_from_exception(err, 403, "Access token is invalid")

        return True

    @staticmethod
    def validate_refresh(json) -> bool or Response:
        input_validator = InputValidator()
        input_validator_response = input_validator.validate_desired(desired_keys=['refresh'],
                                                                    json=json)

        if input_validator_response is not True:
            return input_validator_response

        refresh_token = json['refresh']
        token_handler = TokenHandler()

        try:
            token_handler.verify(refresh_token)

        except token_exceptions.TokenIsInvalid as err:
            return make_response_from_exception(err, 403, "Refresh token is invalid")

        return True


class PermissionValidator:
    def validate(self, permissions: list, json) -> bool or Response:
        try:
            self._validate(permissions, json)

        except controller_exceptions.PermissionsNotGrantedError as err:
            return make_response_from_exception(err, 403, str(err))

        return True

    @staticmethod
    def _validate(permissions: list, json) -> bool:
        token_handler = TokenHandler()
        permissions = token_handler.decode(json["access"])["permissions"]

        for perm in permissions:
            if perm not in permissions:
                raise controller_exceptions.PermissionsNotGrantedError("You don't have sufficient permissions")

        return True
