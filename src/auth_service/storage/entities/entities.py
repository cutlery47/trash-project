from dataclasses import dataclass


@dataclass
class Role:
    id: int = None
    name: str = None


@dataclass
class User:
    id: int = None
    role_id: int = None
    email: str = None
    password: str = None
