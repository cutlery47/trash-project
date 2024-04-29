from datetime import timezone, datetime, timedelta
import hashlib
import jwt

from flask import current_app
from email_validator import validate_email

from email_validator import EmailNotValidError
from auth_service.exceptions import service_exceptions


class TokenHandler:
    def __init__(self):
        self.algorithm = "HS256"

    def generate_access(self, id_, email, role, permissions) -> str:
        payload = self._generate_access_payload(id_, email, role, permissions)
        access_token = jwt.encode(payload=payload, algorithm=self.algorithm, key=current_app.secret_key)
        return access_token

    def generate_refresh(self, id_) -> str:
        payload = self._generate_refresh_payload(id_)
        refresh_token = jwt.encode(payload=payload, algorithm=self.algorithm, key=current_app.secret_key)
        return refresh_token

    def verify(self, token):
        try:
            decoded = jwt.decode(token, algorithms=self.algorithm, key=current_app.secret_key)

        except jwt.PyJWTError as err:
            raise service_exceptions.TokenIsInvalid(str(err))

        return decoded

    def decode(self, token) -> dict:
        # simply decodes all the data without any verification
        return jwt.decode(token, algorithms=self.algorithm, key=current_app.secret_key, options={"verify_signature": False})

    @staticmethod
    def _generate_access_payload(id_, email, role, permissions) -> dict:
        return {
            "id": id_,
            "email": email,
            "role": role,
            "permissions": permissions,
            "exp": datetime.now(tz=timezone.utc) + timedelta(hours=1),  # <- expiration time
            "iat": datetime.now(tz=timezone.utc)  # <- time of issuing
        }

    @staticmethod
    def _generate_refresh_payload(id_) -> dict:
        return {
            "id": id_,
            "exp": datetime.now(tz=timezone.utc) + timedelta(weeks=1),
            "iat": datetime.now(tz=timezone.utc)
        }


class PasswordHandler:
    def validate(self, password: str):
        self._validate_length(8, 32, password)
        self._validate_contents(password)
        return password

    @staticmethod
    def hash(plain_password):
        base64_password = plain_password.encode()
        base64_salt = current_app.secret_key.encode()

        hasher = hashlib.sha256()
        hasher.update(base64_salt + base64_password)
        return hasher.hexdigest()

    @staticmethod
    def _validate_length(min_len: int, max_len: int, password: str):
        if len(password) < min_len:
            raise service_exceptions.PasswordLengthInsufficientError("Password is too short")
        elif len(password) > max_len:
            raise service_exceptions.PasswordLengthExceededError("Password is too long")

    @staticmethod
    def _validate_contents(password: str):
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
            raise service_exceptions.PasswordHasNoDigitsError("Password should have digits")
        if has_letters is False:
            raise service_exceptions.PasswordHasNoLettersError("Password should have letters")
        if has_no_spaces is False:
            raise service_exceptions.PasswordHasSpaceSeparatorError("Password should have no space separators")


class EmailHandler:
    @staticmethod
    def validate(email):
        try:
            normalized_email = validate_email(email, check_deliverability=True)
        except EmailNotValidError as err:
            raise service_exceptions.EmailException(str(err))
        return normalized_email.normalized
