import functools

from flask import current_app, make_response, Response, request
from auth_service.services.handlers import TokenHandler

from auth_service.exceptions.controller_exceptions import (RequiredFieldsNotProvidedError, PermissionsNotGrantedError,
                                                           ForbiddenFieldsProvidedError)
from auth_service.exceptions.service_exceptions import TokenIsInvalid


# TODO: email and password validators

# authentication decorator
def access_required(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # checks that access token is present
        # if it is, checks that one is neither expired nor fake
        access_validation_response = TokenValidator.validate_access(request.json)
        if access_validation_response is not True:
            return access_validation_response

        return func(*args, **kwargs)

    return wrapper


def refresh_required(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # checks that refresh token is neither expired nor fake
        # basically the same as above, but for refresh tokens
        refresh_validation_response = TokenValidator.validate_refresh(request.json)
        if refresh_validation_response is not True:
            return refresh_validation_response

        return func(*args, **kwargs)

    return wrapper


# fields decorator
def fields_required(fields: list):
    def fields_decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # checks that all required fields are present
            input_validator_response = InputValidator.validate_required(fields, request.json)
            if input_validator_response is not True:
                return input_validator_response

            return func(*args, **kwargs)

        return wrapper

    return fields_decorator


# permissions decorator
def permissions_required(permissions: list):
    def permissions_decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # checks if user has matching permissions
            if permissions is not None:
                permissions_validator_response = PermissionValidator.has_permissions(permissions, request.json)
                if permissions_validator_response is not True:
                    return permissions_validator_response

            # wrapper function receive 1 to 2 arguments:
            # 1st argument is always the WRAPPED function
            # 2nd argument is optional and IS USER ID
            # if it is present => we have to check if user is allowed to manipulate data by the id
            id_ = None
            if len(args) > 1:
                id_ = args[1]

            # if user id argument was passed -- check for access
            if id_ is not None:
                permissions_validator_response = PermissionValidator.has_access_to_data(id_, request.json)
                if permissions_validator_response is not True:
                    return permissions_validator_response

            return func(*args, **kwargs)

        return wrapper

    return permissions_decorator


def make_response_from_exception(err, status: int, response: str) -> Response:
    # converts error and all its data into a Response object
    if hasattr(err, "__name__"):
        current_app.logger.error(f"{err.__name__}: {response}")
    else:
        current_app.logger.error(f"{type(err).__name__}: {response}")
    return make_response(response, status)


class InputValidator:
    @staticmethod
    def validate_required(required_fields, json) -> bool or Response:
        for field in required_fields:
            # if any of the required fields is not present -- throwing errrrrror
            if not json.get(field):
                return make_response_from_exception(
                    RequiredFieldsNotProvidedError, 400, f"Desired field: \"{field}\" is not provided"
                )

        return True

    @staticmethod
    def validate_forbidden(forbidden_fields, json) -> bool or Response:
        for field in forbidden_fields:
            # if any of the forbidden fields is present -- throwing errror
            if json.get(field):
                return make_response_from_exception(
                    ForbiddenFieldsProvidedError, 400, f"Forbidden field: \"{field}\" is provided"
                )

        return True


class TokenValidator:
    @staticmethod
    def validate_access(json) -> bool or Response:
        input_validator_response = InputValidator.validate_required(required_fields=['access'],
                                                                    json=json)
        if input_validator_response is not True:
            return input_validator_response

        access_token = json['access']

        try:
            TokenHandler().verify(access_token)

        except TokenIsInvalid as err:
            return make_response_from_exception(type(err), 403, "Access token is invalid")

        return True

    @staticmethod
    def validate_refresh(json) -> bool or Response:
        input_validator_response = InputValidator.validate_required(required_fields=['refresh'],
                                                                    json=json)
        if input_validator_response is not True:
            return input_validator_response

        refresh_token = json['refresh']

        try:
            TokenHandler().verify(refresh_token)

        except TokenIsInvalid as err:
            return make_response_from_exception(type(err), 403, "Refresh token is invalid")

        return True


class PermissionValidator:
    @staticmethod
    def has_access_to_data(requested_id: int, json: dict):
        # getting the id field from an access token payload
        # which represents the id of a REQUESTER (the guy who requested the resource)
        requester_id = TokenHandler().decode(json["access"])["id"]

        # checks if user request his own data
        if requester_id != requested_id:
            return make_response_from_exception(
                PermissionsNotGrantedError, 403, "You don't have access to data by specified id"
            )

        return True

    @staticmethod
    def has_permissions(permissions: list, json):
        # getting permissions, stored is access token (permissions of a token bearer)
        token_permissions = TokenHandler().decode(json["access"])["permissions"]

        for perm in permissions:
            # if user doesn't possess any of the required permissions -- throwing error
            if perm not in token_permissions:
                return make_response_from_exception(
                    PermissionsNotGrantedError, 403, "You don't have desired permissions"
                )

        return True