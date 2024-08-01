import functools

from flask import request

from auth_service.validators.token_validator import TokenValidator
from auth_service.validators.input_validator import InputValidator


# checks that access token is neither expired nor fake
def access_required(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        TokenValidator().get_access_token(validate=True)
        return func(*args, **kwargs)
    return wrapper

# checks that access token contains "admin" as a role value
def admin_required(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        TokenValidator().validate_admin()
        return func(*args, **kwargs)
    return wrapper

# checks that requester has access to provided id
def id_access_required(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        TokenValidator().validate_id_access()
        return func(*args, **kwargs)
    return wrapper

# checks that refresh token is neither expired nor fake
def refresh_required(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        TokenValidator().get_refresh_token(validate=True)
        return func(*args, **kwargs)
    return wrapper

# checks that all required fields are present
def fields_required(fields: list):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            InputValidator().validate_required(fields, request.json)
            return func(*args, **kwargs)
        return wrapper
    return decorator


