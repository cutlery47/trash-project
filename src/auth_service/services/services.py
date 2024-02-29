from flask import Request
from builtins import classmethod

from src.auth_service.storage.entities.enitities import User, Role
from src.auth_service.storage.repositories.user_repository import UserRepository

class SignUpService:

    @classmethod
    def __init__(cls, data: ) -> Request: