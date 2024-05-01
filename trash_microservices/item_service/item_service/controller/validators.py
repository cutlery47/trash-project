import functools

from item_service.exceptions.controller_exceptions import HttpMethodNotAllowed

from django.http import HttpRequest

def validate_http_method(request: HttpRequest, allowed_methods: [str]):
    if request.method not in allowed_methods:
        raise HttpMethodNotAllowed
