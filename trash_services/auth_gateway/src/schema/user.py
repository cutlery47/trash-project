from pydantic import BaseModel

class AuthUser(BaseModel):
    email: str
    password: str

class InUser(AuthUser):
    firstname: str
    surname: str

class UpdateUser(BaseModel):
    email: str = None
    password: str = None
    firstname: str = None
    surname: str = None