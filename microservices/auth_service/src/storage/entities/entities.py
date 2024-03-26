from dataclasses import dataclass


@dataclass
class User:
    id: int = None
    role_id: int = None
    email: str = None
    password: str = None

    def __str__(self):
        return f"User: id = {self.id}, role_id={self.role_id}, email={self.email}, password={self.password}"
