class ControllerException(Exception):
    pass

class HttpMethodNotAllowed(ControllerException):
    def __str__(self):
        return "Http Method Not Allowed"
