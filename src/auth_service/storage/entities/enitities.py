from dataclasses import dataclass


@dataclass
class Role:
    id: int
    name: str


@dataclass
class User:
    id: int
    role_id: int
    mail: str
    password: str
