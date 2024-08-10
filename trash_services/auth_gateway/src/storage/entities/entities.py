from dataclasses import dataclass, fields

@dataclass
class User:
    id: int = None
    role: str = None
    email: str = None
    password: str = None
    firstname: str = None
    surname: str = None

    def serialize(self, is_secure: bool = False) -> dict:
        res = dict()
        for el in fields(self):
            attr = el.name
            attr_val = getattr(self, el.name)
            if attr_val is not None and not (is_secure is True and attr == "password"):
                res[attr] = attr_val
        return res

    def __str__(self):
        return f"User: id = {self.id}, role_id={self.role}, email={self.email}, password={self.password}"
