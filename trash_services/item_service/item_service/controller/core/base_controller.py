from abc import ABC, abstractmethod

from item_service.services.core.base_service import BaseService

from fastapi.routing import APIRouter

class BaseController(ABC):

    # each of these two functions execute exactly once.
    # this made me assume that I CAN afford to make them sync.
    # idk, I jus feel like them being async doesn't make much sense,
    # as it will very barely affect application performance
    # --- MAYBE IM WRONG IDK---

    @abstractmethod
    def setup_api(self) -> None:
        """
        Here you would define your routes using APIRouter
        :return: None
        """
        raise NotImplementedError

    @abstractmethod
    def get_api(self) -> APIRouter:
        """
        Returns an instance of APIRouter
        :return: Already set up APIRouter
        """
        raise NotImplementedError
