from dataclasses import dataclass


@dataclass
class User:
    id: int = None
    role: str = None
    email: str = None
    password: str = None

    def __str__(self):
        return f"User: id = {self.id}, role_id={self.role}, email={self.email}, password={self.password}"
