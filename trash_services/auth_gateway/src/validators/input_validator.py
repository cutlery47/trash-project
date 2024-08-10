from src.exceptions.validation_exceptions import RequiredFieldsNotProvided, ForbiddenFieldsAreProvided

class InputValidator:

    @staticmethod
    def validate_required(required_fields, json):
        for field in required_fields:
            if not json.get(field):
                raise RequiredFieldsNotProvided(f"Desired field: \"{field}\" is not provided")

    @staticmethod
    def validate_forbidden(forbidden_fields, json):
        for field in forbidden_fields:
            if json.get(field):
                raise ForbiddenFieldsAreProvided(f"Forbidden field: \"{field}\" is provided")