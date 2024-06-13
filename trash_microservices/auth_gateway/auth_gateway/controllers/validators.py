import functools

from flask import current_app, make_response, Response, request
from auth_gateway.services.handlers import TokenHandler

from auth_gateway.exceptions.controller_exceptions import (RequiredFieldsNotProvidedError, NotAllowedToAccessResource,
                                                           ForbiddenFieldsProvidedError)
from auth_gateway.exceptions.service_exceptions import TokenIsInvalid, AdminRoleRequired


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
                    RequiredFieldsNotProvidedError, 422, f"Desired field: \"{field}\" is not provided"
                )
        return True

    @staticmethod
    def validate_forbidden(forbidden_fields, json) -> bool or Response:
        for field in forbidden_fields:
            # if any of the forbidden fields is present -- throwing errror
            if json.get(field):
                return make_response_from_exception(
                    ForbiddenFieldsProvidedError, 422, f"Forbidden field: \"{field}\" is provided"
                )
        return True


class TokenValidator:
    @staticmethod
    def validate_access() -> bool or Response:
        access_token = request.cookies.get('access')

        if not access_token:
            return make_response_from_exception(
                RequiredFieldsNotProvidedError, 401, f"Access token is required"
            )

        try:
            TokenHandler().verify(access_token)
        except TokenIsInvalid as err:
            return make_response_from_exception(type(err), 403, "Access token is invalid")
        return True

    @staticmethod
    def validate_admin() -> bool or Response:
        access_token = request.cookies.get('access')
        try:
            TokenHandler().verify_admin(access_token)
        except AdminRoleRequired as err:
            return make_response_from_exception(type(err), 403, "Admin role is required")
        return True

    @staticmethod
    def validate_refresh() -> bool or Response:
        refresh_token = request.cookies.get('refresh')

        if not refresh_token:
            return make_response_from_exception(
                RequiredFieldsNotProvidedError, 401, f"Refresh token is required"
            )

        try:
            TokenHandler().verify(refresh_token)
        except TokenIsInvalid as err:
            return make_response_from_exception(type(err), 401, "Refresh token is invalid")

        return True

    @staticmethod
    def validate_id_access() -> bool or Response:
        access_token = request.cookies.get('access')
        decoded = TokenHandler().decode(access_token)

        token_id = str(decoded.get('id'))
        requested_id = request.url.split('/')[-1]

        if token_id != requested_id:
            return make_response_from_exception(NotAllowedToAccessResource,
                                                401, "You are not allowed to access this resource")
        return True


