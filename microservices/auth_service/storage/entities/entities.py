from dataclasses import dataclass


@dataclass
class Role:
    id: int = None
    name: str = None

    def __str__(self):
        return f"Role: id = {self.id}, name={self.name}"


@dataclass
class User:
    id: int = None
    role_id: int = None
    email: str = None
    password: str = None

    def __str__(self):
        return f"User: id = {self.id}, role_id={self.role_id}, email={self.email}, password={self.password}"
