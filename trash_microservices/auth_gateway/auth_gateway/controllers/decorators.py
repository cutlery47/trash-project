import functools

from flask import request

from auth_gateway.controllers.validators import TokenValidator, InputValidator


# decorator for access validation
def access_required(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # checks that access token is present
        # if it is, checks that one is neither expired nor fake
        access_validation_response = TokenValidator.validate_access()
        if access_validation_response is not True:
            return access_validation_response
        return func(*args, **kwargs)
    return wrapper

# decorator for admin role validation
def admin_required(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        admin_validation_response = TokenValidator.validate_admin()
        if admin_validation_response is not True:
            return admin_validation_response
        return func(*args, **kwargs)
    return wrapper

# decorator for refresh token validation
def refresh_required(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # checks that refresh token is neither expired nor fake
        # basically the same as above, but for refresh tokens
        refresh_validation_response = TokenValidator.validate_refresh()
        if refresh_validation_response is not True:
            return refresh_validation_response
        return func(*args, **kwargs)
    return wrapper

# decorator for present fields validation
def fields_required(fields: list):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # checks that all required fields are present
            input_validator_response = InputValidator.validate_required(fields, request.json)
            if input_validator_response is not True:
                return input_validator_response
            return func(*args, **kwargs)
        return wrapper
    return decorator

# decorator for checking if user has access to the provided id
def id_access_required(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        id_access_validator_response = TokenValidator.validate_id_access()
        if id_access_validator_response is not True:
            return id_access_validator_response
        return func(*args, **kwargs)
    return wrapper

