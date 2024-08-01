from email_validator import validate_email, EmailNotValidError

from auth_service.exceptions.validation_exceptions import PasswordCantBeCreated, EmailIsInvalid

class CredentialsValidator:

    def validate_password(self, password: str):
        self._validate_password_length(8, 32, password)
        self._validate_password_contents(password)
        return password

    @staticmethod
    def _validate_password_length(min_len: int, max_len: int, password: str):
        if len(password) < min_len:
            raise PasswordCantBeCreated("Password is too short")
        elif len(password) > max_len:
            raise PasswordCantBeCreated("Password is too long")

    @staticmethod
    def _validate_password_contents(password: str):
        has_digits = False
        has_letters = False
        has_no_spaces = True

        for char in password:
            if 48 <= ord(char) <= 57 and not has_digits:
                has_digits = True
            elif (65 <= ord(char) <= 90 or 97 <= ord(char) <= 122) and not has_letters:
                has_letters = True
            elif ord(char) == 32 and has_no_spaces:
                has_no_spaces = False

        if has_digits is False:
            raise PasswordCantBeCreated("Password should have digits")
        if has_letters is False:
            raise PasswordCantBeCreated("Password should have letters")
        if has_no_spaces is False:
            raise PasswordCantBeCreated("Password should have no space separators")

    @staticmethod
    def validate_email(email: str) -> str:
        try:
            normalized_email = validate_email(email, check_deliverability=True)
        except EmailNotValidError as err:
            raise EmailIsInvalid(str(err))

        return normalized_email.normalized
