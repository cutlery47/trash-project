from flask import current_app

import hashlib

class PasswordHasher:

    @staticmethod
    def hash(plain_password):
        base64_password = plain_password.encode()
        base64_salt = current_app.secret_key.encode()

        hasher = hashlib.sha256()
        hasher.update(base64_salt + base64_password)
        return hasher.hexdigest()
