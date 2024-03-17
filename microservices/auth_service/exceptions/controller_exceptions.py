class ControllerError(Exception):
    pass


class DesiredFieldsNotProvidedError(ControllerError):
    pass


class ForbiddenFieldsProvidedError(ControllerError):
    pass