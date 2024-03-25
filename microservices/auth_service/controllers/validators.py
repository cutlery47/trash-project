import functools

from flask import current_app, make_response, Response, request

from microservices.auth_service.exceptions import controller_exceptions, token_exceptions
from microservices.auth_service.services.token_handler import TokenHandler

# TODO: clean up this mes


# authentication decorator
def authentication_required(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        token_validator = TokenValidator()
        json = request.json

        access_validation_response = token_validator.validate_access(json)
        if access_validation_response is not True:
            return access_validation_response

        return func(*args, **kwargs)
    return wrapper


def refresh_required(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        token_validator = TokenValidator()
        json = request.json

        refresh_validation_response = token_validator.validate_refresh(json)
        if refresh_validation_response is not True:
            return refresh_validation_response

        return func(*args, **kwargs)
    return wrapper


# permissions decorator
def permissions_required(permissions: list):
    def permissions_decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            permissions_validator = PermissionValidator()
            json = request.json
            id_ = None

            # check if user has matching permissions
            if permissions is not None:
                permissions_validator_response = permissions_validator.has_permissions(permissions, json)
                if permissions_validator_response is not True:
                    return permissions_validator_response

            # wrapper function receive 1 to 2 arguments:
            # 1st argument is always the WRAPPED function
            # 2nd argument is optional and IS USER ID
            # if it is present => we have to check if user is allowed to manipulate data by the id
            if len(args) > 1:
                id_ = args[1]

            if id_ is not None:
                permissions_validator_response = permissions_validator.has_access_to_data(id_, json)
                if permissions_validator_response is not True:
                    return permissions_validator_response

            return func(*args, **kwargs)
        return wrapper
    return permissions_decorator


# input decorator
def fields_required(fields: list):
    def fields_decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            input_validator = InputValidator()
            json = request.json

            input_validator_response = input_validator.validate_required(fields, json)
            if input_validator_response is not None:
                return input_validator_response

            return func(*args, **kwargs)
        return wrapper
    return fields_decorator


def make_response_from_exception(err: Exception, status: int, response: str) -> Response:
    current_app.logger.error(f"{type(err).__name__}: {str(err)}")
    return make_response(response, status)


class InputValidator:
    def validate_required(self, required_fields, json) -> bool or Response:
        # checks that each key is present in the request body
        try:
            self._required_fields_provided(required_fields, json)

        except (controller_exceptions.DesiredFieldsNotProvidedError,
                controller_exceptions.ForbiddenFieldsProvidedError) as err:
            return make_response_from_exception(err, 400, str(err))

        return True

    def validate_forbidden(self, forbidden_fields, json) -> bool or Response:
        # checks that no extra keys are present in the request body
        try:
            self._forbidden_fields_not_provided(forbidden_fields, json)

        except (controller_exceptions.DesiredFieldsNotProvidedError,
                controller_exceptions.ForbiddenFieldsProvidedError) as err:
            return make_response_from_exception(err, 400, str(err))

        return True

    @staticmethod
    def _required_fields_provided(required_fields: list, json: dict):
        for field in required_fields:
            if not json.get(field):
                raise controller_exceptions.DesiredFieldsNotProvidedError(f"Desired key: \"{field}\" is not provided")

        return True

    @staticmethod
    def _forbidden_fields_not_provided(forbidden_fields: list, json: dict):
        for field in forbidden_fields:
            if json.get(field):
                raise controller_exceptions.ForbiddenFieldsProvidedError(f"Forbidden key: \"{field}\" is provided")

        return True


class TokenValidator:
    @staticmethod
    def validate_access(json) -> bool or Response:
        input_validator = InputValidator()
        input_validator_response = input_validator.validate_required(required_fields=['access'],
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
        input_validator_response = input_validator.validate_required(required_fields=['refresh'],
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
    def has_access_to_data(self, requested_id: int, json: dict):
        try:
            self._has_access_to_data(requested_id, json)

        except controller_exceptions.PermissionsNotGrantedError as err:
            return make_response_from_exception(err, 403, str(err))

        return True

    def has_permissions(self, permissions: list, json) -> bool or Response:
        try:
            self._has_permissions(permissions, json)

        except controller_exceptions.PermissionsNotGrantedError as err:
            return make_response_from_exception(err, 403, str(err))

        return True

    @staticmethod
    def _has_access_to_data(requested_id, json):
        token_handler = TokenHandler()
        requester_id = token_handler.decode(json["access"])["id"]

        if requester_id != requested_id:
            raise controller_exceptions.PermissionsNotGrantedError("You don't have access to data by specified id")

    @staticmethod
    def _has_permissions(permissions: list, json):
        token_handler = TokenHandler()
        token_permissions = token_handler.decode(json["access"])["permissions"]

        for perm in permissions:
            if perm not in token_permissions:
                raise controller_exceptions.PermissionsNotGrantedError("You don't have desired permissions")
