class ControllerError(Exception):
    pass


class RequiredFieldsNotProvidedError(ControllerError):
    pass


class ForbiddenFieldsProvidedError(ControllerError):
    pass


class NotAllowedToAccessResource(Exception):
    pass
